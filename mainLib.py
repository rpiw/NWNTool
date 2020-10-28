"""
    This is a main module for the project. Run program from run.py file
"""
from enum import Enum, unique
import pathlib
import os
from typing import List, Any

from exceptions import UnknownVersionException
from exceptions import DirectoryDoesNotExistsException
import pickle
import logging
import scrapper
import zipfile
import cmd
from session import Session

logger = logging.getLogger(__name__)
session = Session()


class GlobalNameSpace:
    u"""Class for keeping everything not fitting to other classes."""
    known_versions = {0: "diamond_edition",
                      1: "enhanced_edition"
                      }
    file_with_saved_modules = "modules_bin"
    install_directory = "."

    @staticmethod
    def check_path(path):
        p = pathlib.Path(path)
        exists, is_directory = False, False
        try:
            exists = p.exists()
            is_directory = p.is_dir()
        except OSError:
            return ""
        finally:
            if exists and is_directory:
                return path
            return ""


class Directory:
    u"""Represent a directory."""

    def __init__(self, path):
        p = pathlib.Path(path)
        if not p.exists():
            raise DirectoryDoesNotExistsException
        else:
            self.path = p
            self.listdir = []

            with os.scandir(self.path) as it:
                for entry in it:
                    self.listdir.append(self.path.joinpath(pathlib.Path(entry.name)))
        self.empty = False if len(self.listdir) > 0 else True


class Config:
    u"""Config file."""
    _keys = ("system",
             "diamond_version", "diamond_version_local_dir",
             "enhanced_version", "enhanced_version_local_dir",
             "tool_directory")

    _instance = None

    @staticmethod
    def initialize(file="config.json"):
        if Config._instance:
            return
        else:
            Config._instance = Config(file)
        return None

    def __init__(self, file="config.json"):
        self._config = {}
        self._file = file
        self._working_dir = os.getcwd()
        self._module_dir = self._working_dir + "/modules"
        self.system_type = {0: "linux", 1: "windows", 2: "macOS"}
        self.system = self.system_type[1]
        self.diamond_version = ""
        self.enhanced_version = ""
        self.diamond_version_local_dir = ""
        self.enhanced_version_local_dir = ""

        self.read_config_file()
        logger.debug("Creating config from file: {0}".format(
            pathlib.Path(os.getcwd()).joinpath(file)))
        Config._instance = self

    def get_modules_dir(self):
        return self._module_dir

    def get_dict(self):
        return self._config

    def read_config_file(self):
        import json
        try:
            with open(self._file, "r") as f:
                self.set_config(json.load(f))
        except FileNotFoundError:
            logging.error("File config not found! Using default settings!")
        return None

    def set_config(self, _cfg):
        self._config = _cfg
        self.system = _cfg[Config._keys[0]]
        self.diamond_version = _cfg[Config._keys[1]]
        self.diamond_version_local_dir = _cfg[Config._keys[2]]
        self.enhanced_version = _cfg[Config._keys[3]]
        self.enhanced_version_local_dir = _cfg[Config._keys[4]]
        self._working_dir = _cfg[Config._keys[5]]
        return None

    @classmethod
    def get_config(cls):
        if Config._instance:
            return Config._instance
        else:
            return Config()

    def pwd(self):
        return self._working_dir

    def print_properties(self):
        print(self.system,
              self.diamond_version, self.diamond_version_local_dir,
              self.enhanced_version, self.enhanced_version_local_dir)


class NWNConfig:

    def __init__(self, path_to_install_dir, path_to_local_dir):
        self.dir_install = pathlib.Path(path_to_install_dir)
        self.dir_local = pathlib.Path(path_to_local_dir)


class Pair:

    def __init__(self, first=None, second=None):
        self.first = first
        self.second = second

    def __setitem__(self, key, value):
        if not isinstance(key, int):
            raise TypeError
        if key == 0:
            self.first = value
        elif key == 1:
            self.second = value
        else:
            raise IndexError

    def __getitem__(self, item):
        if item == 0:
            return self.first
        elif item == 1:
            return self.second
        else:
            raise IndexError

    def not_none(self):
        if self.first and self.second:
            return True
        return False


class NWN:
    u"""Class recognizing type of the game."""
    _instances: List[Any] = []

    @session.register
    def __init__(self, nwn_config: NWNConfig, version: str):
        if not isinstance(nwn_config, NWNConfig):
            return
        self.cfg = nwn_config
        try:
            self.version = NWN.check_version(version)
        except UnknownVersionException:
            self.version = ""

        self.directory_install = Directory(self.cfg.dir_install)
        self.directory_local = Directory(self.cfg.dir_local)

        self.directories = list(d for d in self.directory_install.listdir if pathlib.Path(d).is_dir())
        self.files = list(d for d in self.directory_install.listdir if pathlib.Path(d).is_file())

        self._saved_modules_bin = pathlib.Path(".")  # for serialization with pickle
        self._modules = {"local": self.find_modules(self.directory_local),
                         "install": [self.find_modules(self.directory_install)]}

        self.modules = list(self._modules["local"] + self._modules["install"])
        NWN._instances.append(self)

    @staticmethod
    def show_instances():
        return NWN._instances

    @classmethod
    def find_modules(cls, directory: Directory):
        results = []
        iterator = []
        for d in directory.listdir:
            if d.name == "modules":  # Standard for all NWN versions!
                iterator = os.scandir(directory.path.joinpath(pathlib.Path("modules")))
        for m in iterator:
            if str(m.name).endswith(".mod"):
                module = ModuleInDir(m)
                module.name = "".join(n[0] for n in m.name.split())
                module.title = m.name.replace(".mod", "")
                module.path = m.path
                results.append(module)
        logger.info("Found {0} modules at {1}.".format(len(results), directory.path))

        return results

    def save_module(self, module):
        self.modules.append(module)

    def save_module_unique(self, module):
        if all([module.__ne__(x) for x in self.modules]):
            self.modules.append(module)

    def save_modules_list_to_file(self, filename):
        pickle.dumps(self.modules, filename)

    def load_modules_list(self, filename):
        self.modules = pickle.load(filename)

    def show_modules(self):
        return self.modules

    @staticmethod
    def download_module_from_vault(www: str, name: str) -> scrapper.ScrappedModule:
        module = scrapper.download_module_from_website(www)
        path = Config().get_config().pwd() + "/" + name
        output_path = Config().get_config().get_modules_dir()
        module.save_file(path)

        # detect type of compression
        import re
        comp = module.compression
        if re.search("7z", comp):
            from pyunpack import Archive
            Archive(path).extractall(output_path)
        elif re.search("zip", comp):
            with zipfile.ZipFile(path, "r") as file:
                file.extractall(output_path)
        elif re.search("rar", comp):
            import rarfile
            with rarfile.RarFile(path) as rf:
                rf.extractall(output_path)
        else:
            logger.error("Could NOT decompress the file!")
            from exceptions import UnknownCompressionException
            raise UnknownCompressionException

        logger.info("Successfully decompressed file.")
        return module

    @staticmethod
    def create_module_from_scrapper_data(module_data: scrapper.ScrappedModule):
        path = pathlib.Path(Config().get_modules_dir()).joinpath(module_data.name)
        m = ModuleInDir(path)
        m.name = module_data.kwargs["kwargs"]["title"]
        m.title = m.name
        m.author = module_data.kwargs["kwargs"]["author"]
        m.tags = module_data.kwargs["kwargs"]["tags"]
        logger.debug("Creating module {} from scrapped data {}.".format(m.name, module_data.name))

        return m

    @staticmethod
    def check_version(version):
        if version not in GlobalNameSpace.known_versions.values():
            raise UnknownVersionException(version)
        else:
            return version


class File:
    u"""General representation of Neverwinter Nights file."""

    @unique
    class FileType(Enum):
        module = 0
        hakpack = 1
        music = 2
        movie = 3

    _type = [FileType.module, FileType.hakpack, FileType.music, FileType.movie]

    _extensions = {FileType.module: "mod",
                   FileType.hakpack: "hak",
                   FileType.music: "bmu",
                   FileType.movie: "bik"
                   }

    def __init__(self, path: pathlib.Path):
        self.file = path
        self.size = os.path.getsize(self.file)
        self._ext = path.suffix

    def show_extensions(self):
        return self._ext


class Person:

    def __init__(self, name, surname=""):
        self.name = name
        self.surname = surname

    def __repr__(self):
        print(self.name + " " + self.surname)


class Module:
    u"""Represent a module of Neverwinter Nights game. NWN module's file ends with .mod extension."""
    default = {"name": "Module name", "title": "Module title", "is_part_of_series": False,
               "compatibility": {"Diamond_edition": True, "Enhanced_edition": False},
               "series": None, "dependencies": {File.FileType.hakpack: [],
                                                File.FileType.movie: [],
                                                File.FileType.music: []},
               "cep": False, "cep_version": 0.0, "author": Person("Unknown", "Name"), "tags": [],
               "language": "unknown", "version": -1.00}

    extension = File.FileType.module

    def __init__(self, name="Unknown Module Name"):
        self.name: str = name
        self.title: str = "Title"
        self.is_part_of_series: bool = False
        self.compatibility = {"Diamond_edition": True, "Enhanced_edition": False}
        self.series: str = "Series" if self.is_part_of_series else None
        self.requirements = {"OC": True, "Xp1": True, "Xp2": True}
        self.dependencies = {File.FileType.hakpack: [],
                             File.FileType.movie: [],
                             File.FileType.music: []}
        self.cep: bool = False  # Community expansion pack required
        self.cep_version: float = 2.65 if self.cep else 0
        self.author: Person = Person("Unknown", "Author")
        self.tags = []
        self.language = "English"
        self.version: float = 1.00
        self._up_to_date = False

    def __repr__(self):
        return "Module(Name: {0}, Title: {1})".format(self.name, self.title)

    def __str__(self):
        return "Module title: {0}".format(self.title)

    def __eq__(self, other):
        return self.title == other.title and self.version == other.version

    def __ne__(self, other):
        return not self == other

    def is_up_to_date(self):
        if not self._up_to_date:
            for (attribute, default_attribute) in zip(self.__dict__.keys(), Module.default.keys()):
                if self.__dict__[attribute] == Module.default[default_attribute]:
                    return False
        self._up_to_date = True
        return True


class ModuleInDir(Module):
    u"""Represent a module inside game directory."""

    def __init__(self, path=pathlib.Path()):
        self.path = path
        super(ModuleInDir, self).__init__()


class ModuleInVault(Module):
    u"""Represent a module on a website."""

    def __init__(self, address):
        self.www = address
        self.file_address = ""
        super(ModuleInVault, self).__init__()


class OwnedModules:
    u"""Represent a list of owned modules inside game directory."""

    def __init__(self, list_of_modules=None):
        if list_of_modules is None:
            list_of_modules = []
        self._modules = []
        for module in list_of_modules:
            m = ModuleInDir(".")
            m.name = str(module)

    def add_module(self, module) -> None:
        self._modules.append(module)

    def remove_module(self, module) -> bool:
        if module in self._modules:
            self._modules.remove(module)
            return True
        return False

    def print(self):
        for m in self._modules:
            string = "Name: {0}, title: {1}".format(m.name, m.title)
            print(string)

    def print_paths(self):
        for m in self._modules:
            string = "Name: {0}, path: {1}".format(m.name, m.path)
            print(string)


class Shell(cmd.Cmd):
    intro = "Welcome in NWNTool, type help for help."
    prompt = "NWNTool "
    file = None

    def do_help(self, arg: str) -> None:
        # TODO
        print("It does not work.")

    @staticmethod
    def do_show_modules(*args, **kwargs):
        nwn = NWN.show_instances()
        if len(nwn) == 0:
            print("No modules were found. Run 'find' command to find any NWN directories.")
        else:
            for n in nwn:
                print(n.show_modules(), sep="\n")

    def do_find(self, *args, **kwargs):
        pass

    @staticmethod
    def do_exit(*args, **kwargs):
        return True

    @staticmethod
    def emptyline(*args, **kwargs) -> bool:
        return False

    @staticmethod
    def do_show_register(*args, **kwargs):
        if session.debug:
            print("Tracked objects: ")
            print(session.tracked_objects, sep="\n")
            print("Tracked functions: ")
            print(session.tracked_functions, sep="\n")
            print("Tracked directories: ")
            print(session.tracked_directories, sep="\n")


def main():
    cfg = Config()
    cfg.read_config_file()
    c = cfg.get_dict()

    # Diamond Edition from gog
    cfg_diamond = NWNConfig(c["diamond_version"],
                            c["diamond_version_local_dir"])
    nwn_diamond = NWN(cfg_diamond, GlobalNameSpace.known_versions[0])

    # Enhanced Edition from Steam
    cfg_ee = NWNConfig(c["enhanced_version"],
                       c["enhanced_version_local_dir"])
    nwn_ee = NWN(cfg_ee, GlobalNameSpace.known_versions[1])

    return nwn_diamond, nwn_ee


if __name__ == '__main__':
    main()
