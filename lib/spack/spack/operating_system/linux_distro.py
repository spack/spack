import platform as py_platform
import spack
from spack.architecture import Platform, OperatingSystem

class LinuxDistro(OperatingSystem):
    """ This class will represent the autodetected operating system
        for a Linux System. Since there are many different flavors of
        Linux, this class will attempt to encompass them all through
        autodetection using the python module platform and the method
        platform.dist()
    """
    def __init__(self):
        def detect_operating_system():
            name = py_platform.dist()[0]
            version = py_platform.dist()[1]
            return name, version

        name, version = detect_operating_system()
            
        super(LinuxDistro, self).__init__(name, version, "PATH")
    
    def compiler_strategy(self):
        return self.compiler_strategy

    def find_compilers(self):
        pass

    

