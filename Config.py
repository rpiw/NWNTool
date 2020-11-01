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
        home = pathlib.Path.home()
        self.path = path if pathlib.Path(path).is_absolute() \
            else pathlib.Path.joinpath(home, path)  # Path to main game directory
        self.path_to_local_vault = path_local if pathlib.Path(path).is_absolute()\
            else pathlib.Path.joinpath(home, path_local)

        self.executable = self.find_exe()  # Game executable
        self.modules_directory = None  # Directory containing modules of the game
        self.hak = None  # Hakpacks

    def __repr__(self):
        return "Game Config:\nEdition: {0},\nversion: {1},\npath to main dir: {2},\npath to local: {3},\nmodules dir: {4},\nmain exe: {5}".format(
            self.edition, self.version, self.path,
            self.path_to_local_vault, self.modules_directory, self.executable
        )

    def find_exe(self):
        exe = ""
        if self.edition.lower() == "diamond_edition":
            exe = "nwmain.exe"
        elif self.edition.lower() == "enhanced_edition":
            if platform.system().lower() == "linux":
                exe = "bin/linux-x86/nwmain-linux"
            elif platform.system().lower() == "windows":
                exe = "bin/win32/nwmain.exe"
        exe = pathlib.Path.joinpath(self.path, exe)
        return pathlib.Path.joinpath(pathlib.Path.home(), exe)


class ProgramConfig:
    u"""Contains program configuration. Init with path to working directory. If none, current directory is used."""
    def __init__(self, directory=None):
        self.main_directory = directory if not directory else os.getcwd()  # Directory where all data is saved by a default
        self.config_file = ""  # File with config info, JSON
        self.modules_list_file = ""  # File with listed modules found in game's directory
        self.modules_list_in_vault_file = ""  # File with all modules names and www address to them
        self.history_file = ""  # File with history of user's action, by default should be in main directory
        self.modules = "modules"

    def __repr__(self):
        return """Program Config: main directory: {0}, stored config: {1}, modules list: {2}, modules list on vault:
         {3}""".format(self.main_directory, self.config_file, self.modules_list_file, self.modules_list_in_vault_file)


class Config:
    u"""General representation of all configuration info."""
    def __init__(self, game_cfg, program_cfg):
        self.game_config = game_cfg
        self.program_config = program_cfg

    def __repr__(self):
        return "\n".join((repr(self.game_config), repr(self.program_config)))


class CurrentConfig(metaclass=singleton.Singleton):
    u"""Singleton to store currently used configuration."""
    def __init__(self, cfg=None):
        self._config = cfg if cfg is not None else ConfigFactory().create()

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, new_cfg):
        if new_cfg is Config:
            self._config = new_cfg
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


class CreateConfigFromStdStream(AbstractConfigFactory):
    def create(self, *args, **kwargs):
        u"""Create config object and save to a file. Data is entered by a user via standard input."""
        _exit = False

        print("Interactive config creation procedure. You are welcome, human being!")

        while not _exit:
            try:
                _input = input()
                if "exit" == _input:
                    print("Exiting to CLI")
                    logger.debug("Exit config creation.")
                    _exit = True
            except TypeError:
                print("""Wrong path provided, try again or type 'exit' the dialog and return to CLI
                 or press Ctrl+C to abort.""")


# ############################ Default ##############################
prog = ProgramConfig(".")
game = GameConfig("Diamond_Edition", "1.69", default_linux[0], default_linux[1])
c = Config(game, prog)
config = CurrentConfig(c)
