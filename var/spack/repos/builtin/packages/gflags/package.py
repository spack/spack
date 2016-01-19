import os
from spack import *

class Gflags(Package):
    """The gflags package contains a C++ library that implements
    commandline flags processing. It includes built-in support for
    standard types such as string and the ability to define flags
    in the source file in which they are used. Online documentation
    available at: https://gflags.github.io/gflags/"""

    homepage = "https://gflags.github.io/gflags"
    url      = "https://github.com/gflags/gflags/archive/v2.1.2.tar.gz"

    version('2.1.2', 'ac432de923f9de1e9780b5254884599f')

    def install(self, spec, prefix):
        cmake("-DCMAKE_INSTALL_PREFIX=" + prefix,
              "-DBUILD_SHARED_LIBS=ON")
        make()
        make("test")
        make("install")
