import re
import platform as py_platform
from spack.architecture import OperatingSystem


class BgqDistro(OperatingSystem):
    """ This class will represent the autodetected operating system
        for a Linux System. Since there are many different flavors of
        Linux, this class will attempt to encompass them all through
        autodetection using the python module platform and the method
        platform.dist()
    """

    def __init__(self):
        name = 'CNK'
        version = '1'
        super(BgqDistro, self).__init__(name, version)

    def __str__(self):
        return self.name
