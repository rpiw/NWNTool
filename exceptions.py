class UnknownVersionException(Exception):
    """Raised when passed unrecognized argument 'version' to NWN class initializer.
    Attributes:
        version -- wrong argument passed to initializer.
    """
    def __init__(self, version):
        self.version = version
        self.message = "Unrecognized version of Neverwinter Nights: {0}".format(self.version)
        super().__init__(self.message)
