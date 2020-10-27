import logging

logger = logging.getLogger(__name__)


class GeneralException(Exception):

    def __init__(self, message: str):
        logger.error(message)
        super(GeneralException, self).__init__()


class UnknownVersionException(GeneralException):
    """Raised when passed unrecognized argument 'version' to NWN class initializer.
    Attributes:
        version -- wrong argument passed to initializer."""
    def __init__(self, version):
        super(UnknownVersionException, self).__init__(
            "Unrecognized version of Neverwinter Nights: {0}".format(version))


class DirectoryDoesNotExistsException(GeneralException):
    """Raised when passed not existing path to a Directory class' initializer."""
    def __init__(self, path):
        super(DirectoryDoesNotExistsException, self).__init__(
            "Directory does not exists: {0}".format(path))


class InvalidUrl(GeneralException):
    """Invalid url was provided."""
    def __init__(self):
        super(InvalidUrl, self).__init__("Address of website is not valid!")


class UnknownCompressionException(GeneralException):
    u"""Unknown extension of compressed file."""
    def __init__(self):
        super(UnknownCompressionException, self).__init__("Unknown extension of compressed file")
