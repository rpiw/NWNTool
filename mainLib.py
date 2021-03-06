"""
    This is a main module for the project. Run program from run.py file
"""
from enum import Enum, unique
import pathlib
import os
from typing import List, Any
import re
from exceptions import UnknownVersionException
import pickle
import logging
import scrapper
import zipfile
import cmd

from session import Session
import Config


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


class NWN:
    u"""Class recognizing type of the game."""
    _instances: List[Any] = []

    @session.register
    def __init__(self, cfg=None):
        if cfg is None:
            cfg = Config.config.config
        self.directory_install = cfg.game_config.path
        self.directory_local = cfg.game_config.path_to_local_vault

        self.directories = list(d for d in os.scandir(self.directory_install) if pathlib.Path(d).is_dir())
        self.files = list(d for d in os.scandir(self.directory_install) if pathlib.Path(d).is_file())

        self._saved_modules_bin = pathlib.Path(".")  # for serialization with pickle
        self._modules = {"local": self.find_modules(self.directory_local),
                         "install": [self.find_modules(self.directory_install)]}

        self.modules = list(self._modules["local"] + self._modules["install"])
        NWN._instances.append(self)

    @staticmethod
    def show_instances():
        return NWN._instances

    @classmethod
    def find_modules(cls, directory):
        results = []
        iterator = []
        for d in os.scandir(directory):
            if d.name == "modules":  # Standard for all NWN versions!
                iterator = os.scandir(pathlib.Path.joinpath(directory, pathlib.Path("modules")))
        for m in iterator:
            if str(m.name).endswith(".mod"):
                module = ModuleInDir(m)
                module.name = "".join(n[0] for n in m.name.split())
                module.title = m.name.replace(".mod", "")
                module.path = m.path
                results.append(module)
        logger.info("Found {0} modules at {1}.".format(len(results), directory))

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
        cfg = Config.config
        path = cfg.program_config.main_directory + "/" + name
        output_path = cfg.program_config.modules
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
        path = pathlib.Path(Config.config.program_config.modules).joinpath(module_data.name)
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

    @staticmethod
    def do_modules(*args, **kwargs):
        """Prints all modules found on disk."""
        nwn = NWN.show_instances()
        if len(nwn) == 0:
            print("No modules were found. Run 'find' command to find any NWN directories.")
        else:
            for n in nwn:
                print(n.show_modules(), sep="\n")

    def do_find(self, *args, **kwargs):
        """Find Neverwinter Nights directory."""
        main()

    @staticmethod
    def do_exit(*args, **kwargs):
        """Exit."""
        return True

    @staticmethod
    def emptyline(*args, **kwargs) -> bool:
        return False

    @staticmethod
    def do_register(*args, **kwargs):
        """Shows tracked objects, functions and directories. Works in debug mode only."""
        if session.debug:
            print("Tracked objects: ")
            print(session.tracked_objects, sep="\n")
            print("Tracked functions: ")
            print(session.tracked_functions, sep="\n")
            print("Tracked directories: ")
            print(session.tracked_directories, sep="\n")

    def do_config(self, *args, **kwargs):
        u"""Shows configuration, debug only."""
        for arg in args:
            if arg == "save":
                Config.save()
            if arg == "load":
                Config.config = Config.load()

        print(Config.config.config)

    def do_install(self, *args, **kwargs):
        u"""Run installation."""
        from exceptions import InstallationAbortedException
        force = False
        path = "."
        name = None
        try:
            for kwarg in args:
                if kwarg == "-force":
                    force = True
                if "path=" in kwarg:
                    path = re.split("=", kwarg)[-1]
                if "name=" in kwarg:
                    name = re.split("=", kwarg)[-1]
            Install.install(path=path, force=force, name=name)
        except InstallationAbortedException:
            logger.debug("Installation failed.")

    def do_show_modules_list(self, *args, **kwargs):
        u"""Show list of all modules found in neverwintervault.org.
        :: www, bool - download links from vault,
        :: file, bool  - if True try to read from file,
        :: output, str - name of file to save, if empty string, stdout is used, optionally bool True may be given -
            list is saved to file with default name."""
        modules = []
        www = True
        file = False
        output = ""

        data = dict(args)
        print(data)

        if www:
            modules = scrapper.create_list_of_links()
        elif file:
            try:
                with open(file, "r", encoding="utf-8") as fi:
                    modules = fi.read()
            except FileNotFoundError:
                logger.error("File not found. Given name: {}".format(file))
        else:
            logger.info("You did not specify a source of modules to list from.")
            return

        if output:
            logger.debug("output name: {}".format(output))

            if isinstance(output, str):
                p = pathlib.Path(output)
            elif isinstance(output, bool):
                p = pathlib.Path(Config.MODULES_FILE)

            try:
                force = kwargs["force"]
            except KeyError:
                pass

            if not force:
                if p.exists():
                    return
            with open(p, "w") as fi:
                fi.writelines(modules)

        else:
            if __debug__:
                print("Found some names: {}".format(len(modules)))
            else:
                for m in modules:
                    name = m.rsplit("/", 1)[-1]
                    print(name)

def main():
    nwn = NWN()

    return nwn


class Install:
    @staticmethod
    @session.register
    def install(path=".", name=None, force=False):
        u"""Install the program:
            :path - str, place where the main directory is created, default .,
            :modules_list - bool, if true, download from Vault modules list and save on disk default True"""
        logger.info("Starting installation.")
        from Config import CreateConfigFromStdStream
        exceptions = []
        directory_name = name if name else "NWNTool"

        try:
            if path == ".":
                path = pathlib.Path.cwd()
            directory = pathlib.Path.joinpath(path, pathlib.Path(directory_name))

            if force:
                logger.debug("Attempting to remove directory: {}".format(directory))
                directory.rmdir()

            os.chdir(path)
            logger.debug("Current working directory: {}".format(pathlib.Path.cwd()))
            logger.debug("Target directory: {}".format(directory))

            if directory.is_dir():
                logger.error("This directory should not exist yet...: {}".format(directory.is_dir()))
                logger.info("To force installation in this path use 'install -force',"
                            " this will erase directory and its content")

            logger.debug("Attempting to create a target directory...")
            pathlib.Path.mkdir(directory, parents=True)

            os.chdir(directory)
            from exceptions import CreateConfigFromStdStreamAbortedException
            config = Config.config
            try:
                config = CreateConfigFromStdStream()
            except CreateConfigFromStdStreamAbortedException:
                logger.info("Falling to default settings...")

        except FileNotFoundError as excep:
            logger.error("FileNotFoundError. Probably you missing parent of target directory: {}".format(directory))
            exceptions.append(excep)
        except FileExistsError as excep:
            logger.error("Path is not empty! Directory exists: {}".format(directory))
            exceptions.append(excep)
        except OSError as excep:
            exceptions.append(excep)
        finally:
            if exceptions:
                logger.error("Installation aborted with an exception.")
                from exceptions import InstallationAbortedException
                raise InstallationAbortedException
            else:
                logger.info("Installation completed.")


if __name__ == '__main__':
    main()
