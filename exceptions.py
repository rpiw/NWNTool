import logging

logger = logging.getLogger(__name__)


class GeneralException(Exception):

    def __init__(self, message: str):
        logger.error(message)
        super(GeneralException, self).__init__()


class UnknownVersionException(Exception):
    """Raised when passed unrecognized argument 'version' to NWN class initializer.
    Attributes:
        version -- wrong argument passed to initializer."""
    def __init__(self, version):
        self.message = "Unrecognized version of Neverwinter Nights: {0}".format(version)
        super().__init__(self.message)


class DirectoryDoesNotExistsException(Exception):
    """Raised when passed not existing path to a Directory class' initializer."""
    def __init__(self, path):
        self.message = "Directory does not exists: {0}".format(path)
        super().__init__(self.message)


class InvalidUrl(Exception):
    """Invalid url was provided."""
    def __init__(self):
        self.message = "Address of website is not valid!"
        super(InvalidUrl, self).__init__(self.message)
