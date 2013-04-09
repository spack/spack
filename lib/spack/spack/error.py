
class SpackError(Exception):
    """This is the superclass for all Spack errors.
       Subclasses can be found in the modules they have to do with.
    """
    def __init__(self, message):
        super(SpackError, self).__init__(message)


class UnsupportedPlatformError(SpackError):
    """Raised by packages when a platform is not supported"""
    def __init__(self, message):
        super(UnsupportedPlatformError, self).__init__(message)
