import datetime
from enum import Enum, unique


class Log:
    u"""Maintain writing a log."""
    instances = []

    def __init__(self):
        self.name = "log" + datetime.datetime.now().strftime("%Y_%m_%d_%H%M")
        self.log = []
        Log.instances.append(self)

    def write(self):
        with open(self.name, "a") as log:
            for line in self.log:
                log.write(line + "\n")

    def cache(self, data):
        if data is not str:
            try:
                data = str(data)
            except TypeError:
                data = "Could not convert data to string."
        self.log.append(data)

    @staticmethod
    def show_instances():
        return Log.instances


class GlobalNameSpace:
    u"""Class for keeping everything not fitting to other classes."""
    known_versions = ["enhanced_edition", "diamond_edition"]


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
        self.path = path_to_dir
        self.version = version
        if self.version not in GlobalNameSpace.known_versions:
            from exceptions import UnknownVersionException
            raise UnknownVersionException(self.version)


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
    pass
