# Configure entire program
import singleton
import logging
import os
from collections import namedtuple
import pathlib
import platform

logger = logging.getLogger(__name__)

keys = namedtuple("Keys", ["diamond_version", "diamond_version_local",
                           "enhanced_version", "enhanced_version_local",
                           "working_directory"])

default_config_data = namedtuple("Default_Config", ["linux", "windows"])
default_linux = keys(
                ".wine/drive_c/GOG Games/NWN Diamond",
                ".wine/drive_c/GOG Games/NWN Diamond",
                ".steam/steam/steamapps/common/Neverwinter Nights",
                ".local/share/Neverwinter Nights",
                ".")

default_windows = keys("GOG Games/NWN Diamond",
                       "GOG Games/NWN Diamond",
                       "C://Program Files/steam/steamapps/common/Neverwinter Nights",
                       ".",
                       ".")

cfg = default_config_data(default_linux, default_windows)


class GameConfig:
    u"""Contains game configuration."""
    def __init__(self, game_edition, game_version, path, path_local):
        self.edition = game_edition  # Diamond/Enhanced
        self.version = game_version  # Build version
        self.path = path  # Path to main game directory
        self.path_to_local_vault = path_local
        self.executable = None  # Game executable
        self.modules_directory = None  # Directory containing modules of the game
        self.hak = None  # Hakpacks


class ProgramConfig:
    u"""Contains program configuration. Init with path to working directory. If none, current directory is used."""
    def __init__(self, directory=None):
        self.main_directory = directory if not directory else os.getcwd()  # Directory where all data is saved by a default
        self.config_file = ""  # File with config info, JSON
        self.modules_list_file = ""  # File with listed modules found in game's directory
        self.modules_list_in_vault_file = ""  # File with all modules names and www address to them
        self.history_file = ""  # File with history of user's action, by default should be in main directory
        self.modules = "modules"


class Config:
    u"""General representation of all configuration info."""
    def __init__(self, game_cfg, program_cfg):
        self.game_config = game_cfg
        self.program_config = program_cfg


class CurrentConfig(metaclass=singleton.Singleton):
    u"""Singleton to store currently used configuration."""
    def __init__(self, cfg=None):
        self.__config = cfg if cfg is not None else ConfigFactory().create()

    @property
    def __config(self):
        return self.__config

    @__config.setter
    def __config(self, new_cfg):
        if new_cfg is Config:
            self.__config = new_cfg
            logger.debug("Changing configuration.")

    def save(self, file):
        import json
        with open(file, "w") as fi:
            json.dump(self, fi)


class ExpectedConfig:
    u"""Placeholder for known versions."""
    edition = namedtuple("Edition", ["enhanced_edition", "diamond_edition"])


class AbstractConfigFactory(object):
    def create(self, *args, **kwargs): pass


class DefaultConfigFactory(AbstractConfigFactory):
    def create(self, *args, **kwargs):
        game_edition = "Enhanced Edition"
        game_version = "Release"
        home = pathlib.Path.home()
        OS = platform.system()

        if OS == "Linux":
            path = pathlib.Path.joinpath(home, pathlib.Path("./steam/steam/steamapps/Neverwinter Nights"))
            directory = pathlib.Path.joinpath(home,
                                              pathlib.Path(".local/share"))
        elif OS == "Windows":
            path = pathlib.Path.joinpath(home, "Steam")
            directory = home
        else:
            from exceptions import UnknownOSException
            raise UnknownOSException

        path_local = pathlib.Path.joinpath(directory, pathlib.Path("Neverwinter Nights"))

        game_cfg = GameConfig(game_edition, game_version, path, path_local)
        prog_cfg = ProgramConfig(directory)

        return game_cfg, prog_cfg


class ConfigFactory(AbstractConfigFactory):
    def create(self, *args, **kwargs):
        try:
            game = GameConfig(kwargs["game_edition"],
                              kwargs["game_version"],
                              kwargs["path"])
        except KeyError:
            game, _ = DefaultConfigFactory().create()

        try:
            program = ProgramConfig(kwargs["directory"])
        except KeyError:
            _, program = DefaultConfigFactory().create()

        return Config(game, program)


config = CurrentConfig()
