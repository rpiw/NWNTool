"""
    This is a main module for the project. Run program from run.py file
"""
from enum import Enum, unique
import pathlib
import os
from exceptions import UnknownVersionException
from exceptions import DirectoryDoesNotExistsException
import pickle
import logging

logger = logging.getLogger(__name__)


class GlobalNameSpace:
    u"""Class for keeping everything not fitting to other classes."""
    known_versions = {0: "enhanced_edition", 1: "diamond_edition"}
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


class Config:
    u"""Config file."""
    _keys = ("system",
             "diamond_version", "diamond_version_local_dir",
             "enhanced_version",  "enhanced_version_local_dir")

    def __init__(self, file="config.json"):
        self._config = {}
        self._file = file
        self._working_dir = os.getcwd()
        self.system_type = {0: "linux", 1: "windows", 2: "macOS"}
        self.system = self.system_type[1]
        self.diamond_version = ""
        self.enhanced_version = ""
        self.diamond_version_local_dir = ""
        self.enhanced_version_local_dir = ""

        self.read_config_file()
        logger.debug("Creating config from file: {0}".format(
                                                    pathlib.Path(os.getcwd()).joinpath(file)))

    def read_config_file(self):
        import json
        try:
            with open(self._file, "r") as f:
                self.set_config(json.load(f))
        except FileNotFoundError:
            logging.error("File config not found! Using default settings!")

    def set_config(self, _cfg):
        self._config = _cfg
        self.system = _cfg[Config._keys[0]]
        self.diamond_version = _cfg[Config._keys[1]]
        self.diamond_version_local_dir = _cfg[Config._keys[2]]
        self.enhanced_version = _cfg[Config._keys[3]]
        self.enhanced_version_local_dir = _cfg[Config._keys[4]]

    def get_config(self):
        return self._config

    def print_properties(self):
        print(self.system,
              self.diamond_version, self.diamond_version_local_dir,
              self.enhanced_version, self.enhanced_version_local_dir)


class NWN:
    u"""Class recognizing type of the game."""
    _instance = None

    @staticmethod
    def get_instance():
        if NWN._instance:
            return NWN._instance
        else:
            c = Config.get_config()
            NWN(c["diamond_version_local_dir"], GlobalNameSpace.known_versions[1])

    def __init__(self, path_to_dir, version):
        if NWN._instance:
            return
        self.path = pathlib.Path(GlobalNameSpace.check_path(path_to_dir))
        try:
            self.version = NWN.check_version(version)
        except UnknownVersionException:
            self.version = ""
        self.directory = Directory(self.path)
        self.directories = list(d for d in self.directory.listdir if pathlib.Path(d).is_dir())
        self.files = list(d for d in self.directory.listdir if pathlib.Path(d).is_file())
        self._saved_modules_bin = pathlib.Path(".")
        NWN._instance = self
        self._modules = self.find_modules()

    def find_modules(self):
        results = []
        iterator = []
        for d in self.directories:
            if d.name == "modules":  # Standard for all NWN versions!
                iterator = os.scandir(self.path.joinpath(pathlib.Path("modules")))
        for m in iterator:
            if str(m.name).endswith(".mod"):
                module = ModuleInDir(m)
                module.name = "".join(n[0] for n in m.name.split())
                module.title = m.name.replace(".mod", "")
                module.path = m.path
                results.append(module)
        logger.info("Found {0} modules at {1}.".format(len(results), os.getcwd()))

        return results

    def save_modules(self):
        self._modules = OwnedModules(self.find_modules())

    def save_module(self, module):
        self._modules.append(module)

    def save_module_unique(self, module):
        if all([module.__ne__(x) for x in self._modules]):
            self._modules.append(module)

    def save_modules_list_to_file(self, filename):
        pickle.dumps(self._modules, filename)

    def load_modules_list(self, filename):
        self._modules = pickle.load(filename)

    def show_modules(self):
        return self._modules

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


def main():
    cfg = Config()
    cfg.read_config_file()
    c = cfg.get_config()
    nwn = NWN(c["diamond_version_local_dir"], GlobalNameSpace.known_versions[1])


if __name__ == '__main__':
    main()
