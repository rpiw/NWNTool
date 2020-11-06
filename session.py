import singleton
import os
import logging

logger = logging.getLogger(__name__)


class Session(metaclass=singleton.Singleton):
    u"""Class representing running session. Should collect all info needed for interactive usage."""
    path = os.getcwd()
    debug = False

    def __init__(self):
        self.tracked_directories = []
        self.tracked_objects = {}
        self.tracked_functions = {}

        logger.debug("Starting a new session!")

    def register(self, function):
        self.tracked_functions[function.__name__] = function
        logger.debug("Calling a function: {}".format(function.__name__))
        return function
