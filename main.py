import datetime
from enum import Enum, unique
import pathlib
import os

from exceptions import UnknownVersionException
from exceptions import DirectoryDoesNotExistsException

class Log:
    u"""Maintain writing a log."""
    instances = []
    _limit = 1000  # Amount of characters to cache
    _force = False

    def __init__(self):
        self.name = "log" + datetime.datetime.now().strftime("%Y_%m_%d_%H%M")
        self.log = []
        Log.instances.append(self)

    def write(self):
        with open(self.name, "a") as log:
            for line in self.log:
                l = line + "\n"
                print(l)
                log.write(l)
        self.log.clear()

    def cache(self, data):
        if data is not str:
            try:
                data = str(data)
            except TypeError:
                data = "Could not convert data to string."
        self.log.append(data)
        if len(self.log) >= Log._limit:
            self.write()
            self._force = False
        elif self._force:
            self.write()

    def force_write(self):
        self._force = True

    @staticmethod
    def show_instances():
        return Log.instances


class GlobalNameSpace:
    u"""Class for keeping everything not fitting to other classes."""
    known_versions = {0: "enhanced_edition", 1: "diamond_edition"}

    @staticmethod
    def check_path(path):
        p = pathlib.Path(path)
        try:
            exists = p.exists()
            is_directory = p.is_dir()
        except OSError:
            log.cache("Invalid path.")
            return ""
        finally:
            if exists and is_directory:
                return path
            log.cache("Directory does not exist or path is invalid.")
            return ""


class Config:
    u"""Config file."""
    _keys = ("system",
             "diamond_version", "diamond_version_local_dir",
             "enhanced_version",  "enhanced_version_local_dir")

    def __init__(self, file="config.json"):
        self._config = {}
        self._file = file
        self.system_type = {0: "linux", 1: "windows", 2: "macOS"}
        self.system = self.system_type[1]
        self.diamond_version = ""
        self.enhanced_version = ""
        self.diamond_version_local_dir = ""
        self.enhanced_version_local_dir = ""

    def read_config_file(self):
        import json
        try:
            with open(self._file, "r") as f:
                self.set_config(json.load(f))
        except FileNotFoundError:
            log.cache("Config file not found!")

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
    def __init__(self, path_to_dir, version):
        self.path = GlobalNameSpace.check_path(path_to_dir)
        try:
            self.version = NWN.check_version(version)
        except UnknownVersionException:
            self.version = ""
        self.directory = Directory(self.path)
        self.directories = list(d for d in self.directory.listdir if os.DirEntry.is_dir(d))
        self.files = list(d for d in self.directory.listdir if os.DirEntry.is_file(d))

    @staticmethod
    def check_version(version):
        if version not in GlobalNameSpace.known_versions.values():
            raise UnknownVersionException(version)
        else:
            return version


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
                    self.listdir.append(entry)


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

    def __init__(self, file, directory: Directory):
        self.file = file
        self.directory = directory


if __name__ == '__main__':
    log = Log()
    log.force_write()
    cfg = Config()
    cfg.read_config_file()
    c = cfg.get_config()
    nwn = NWN(c["diamond_version_local_dir"], GlobalNameSpace.known_versions[1])
