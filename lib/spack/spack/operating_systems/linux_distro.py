import platform as py_platform
from spack.architecture import OperatingSystem

class LinuxDistro(OperatingSystem):
    """ This class will represent the autodetected operating system
        for a Linux System. Since there are many different flavors of
        Linux, this class will attempt to encompass them all through
        autodetection using the python module platform and the method
        platform.dist()
    """
    def __init__(self):
        name = py_platform.dist()[0]
        version = py_platform.dist()[1].split(".")[0] # Grabs major version from tuple 

        super(LinuxDistro, self).__init__(name, version)
