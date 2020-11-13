# Configure entire program
import singleton
import logging
import os
import pathlib
import platform
import pickle
logger = logging.getLogger(__name__)

default_linux = (
                ".wine/drive_c/GOG Games/NWN Diamond",
                ".wine/drive_c/GOG Games/NWN Diamond",
                ".steam/steam/steamapps/common/Neverwinter Nights",
                ".local/share/Neverwinter Nights")

default_windows = (r"GOG Games/NWN Diamond",
                   r"GOG Games/NWN Diamond",
                   r"C://Program Files/steam/steamapps/common/Neverwinter Nights",
                   ".")  # idk where

home = pathlib.Path.home()
_join = pathlib.Path.joinpath
_DEFAULT_DATA_EMPTY = False
_CONFIG_FILE_NAME = "config_pickle"

if platform.system() == "Linux":
    default_directory = _join(home, pathlib.Path(r".local/share/NWNTool"))
    default_path = _join(home, pathlib.Path(r".steam/steam/steamapps/common/Neverwinter Nights"))
    default_local_path = _join(home, pathlib.Path(r".local/share/Neverwinter Nights"))
elif platform.system() == "Windows":
    default_directory = _join(home, "NWNTool")
    default_path = _join(home, r"steam/steam/steamapps/common/Neverwinter Nights")
    default_local_path = default_path  # TODO
else:
    default_directory = ""
    default_path = ""
    default_local_path = ""
    _DEFAULT_DATA_EMPTY = True
    logger.error("Unknown OS.")


class GameConfig:
    u"""Contains game configuration."""
    def __init__(self, path, path_local):
        self.path = path if pathlib.Path(path).is_absolute() \
            else pathlib.Path.joinpath(home, path)  # Path to main game directory
        self.path_to_local_vault = path_local if pathlib.Path(path).is_absolute()\
            else pathlib.Path.joinpath(home, path_local)

        # Directory containing modules of the game
        self.modules_directory = pathlib.Path.joinpath(self.path_to_local_vault, "modules")
        # Directory containing hakpacks
        self.hak = pathlib.Path.joinpath(self.path_to_local_vault, "hak")

    def __repr__(self):
        return "Game Config:\npath to main dir: {},\npath to local: {},\nmodules dir: {}".format(
            self.path, self.path_to_local_vault, self.modules_directory
        )


class ProgramConfig:
    u"""Contains program configuration. Init with path to working directory. If none, current directory is used."""
    def __init__(self, directory=None):
        # Directory where all data is saved by a default, NOT GAME DIRECTORY
        self.main_directory = directory if not directory else os.getcwd()
        self.config_file = ""  # File with config info, JSON

    def __repr__(self):
        return """Program Config: main directory: {}, stored config: {}""".format(self.main_directory, self.config_file)


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


class AbstractConfigFactory(object):
    def create(self, *args, **kwargs): pass


class DefaultConfigFactory(AbstractConfigFactory):
    def create(self, *args, **kwargs):
        if _DEFAULT_DATA_EMPTY:
            raise OSError

        game_cfg = GameConfig(default_path, default_local_path)
        prog_cfg = ProgramConfig(default_directory)

        return game_cfg, prog_cfg


class ConfigFactory(AbstractConfigFactory):
    def create(self, *args, **kwargs):
        try:
            game = GameConfig(kwargs["path"], kwargs["path_local"])
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

        questions = ("Enter path to main NWN Diamond Edition directory ",
                     "Enter path to local directory of NWN Diamond Edition",
                     "Enter path to NWN Enhanced Edition main directory",
                     "Enter path to NWN Enhanced Edition local directory")

        i = 0
        question = questions[i]
        answers = ["", "", "", "", "."]

        while not _exit:
            try:
                print(question)
                _input = input()
                path = pathlib.Path(_input)

                if not path.is_absolute():
                    path = pathlib.Path.joinpath(pathlib.Path.cwd(), path)

                answers[i] = str(path)

                if "exit" == _input:
                    print("Exiting to CLI")
                    logger.debug("Exit config creation.")
                    _exit = True

            except TypeError:
                print("""Wrong path provided, try again or type 'exit' the dialog and return to CLI
                 or press Ctrl+C to abort.""")
            if _exit:
                from exceptions import CreateConfigFromStdStreamAbortedException
                raise CreateConfigFromStdStreamAbortedException

            i += 1
            if i == 4:
                break


# Default:
config = CurrentConfig()
MODULES_FILE = "modules_in_vault_list.txt"


def save():
    logger.debug("Attempting to save config.")
    with open(_CONFIG_FILE_NAME, "wb") as fi:
        pickle.dump(config, fi)
    logger.debug("Saved successfully.")


def load():
    r = None
    logger.debug("Attempting to load config.")
    with open(_CONFIG_FILE_NAME, "rb") as fi:
        r = pickle.load(fi)
    logger.debug("Loaded successfully.")
    return r



