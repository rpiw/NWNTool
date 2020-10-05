import datetime
from enum import Enum, unique
import pathlib

from exceptions import UnknownVersionException


class Log:
    u"""Maintain writing a log."""
    instances = []
    _limit = 1000  # Amount of characters to cache

    def __init__(self):
        self.name = "log" + datetime.datetime.now().strftime("%Y_%m_%d_%H%M")
        self.log = []
        Log.instances.append(self)

    def write(self):
        with open(self.name, "a") as log:
            for line in self.log:
                log.write(line + "\n")
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

    @staticmethod
    def show_instances():
        return Log.instances


class GlobalNameSpace:
    u"""Class for keeping everything not fitting to other classes."""
    known_versions = {0: "enhanced_edition", 1: "diamond_edition"}


class Config:
    u"""Config file."""

    def __init__(self):
        self.system_type = {0: "linux", 1: "windows", 2: "macOS"}
        self.system = self.system_type[0]
        self.diamond_version = None
        self.enhanced_version = None


class NWN:
    u"""Class recognizing type of the game."""
    def __init__(self, path_to_dir, version):
        self.path = NWN.check_path(path_to_dir)
        try:
            self.version = NWN.check_version(version)
        except UnknownVersionException:
            self.version = ""
        self.directories = []

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

    def __init__(self, file):
        self.file = file


if __name__ == '__main__':
    log = Log()


