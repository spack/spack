#------------------------------------------------------------------------------
# Author: Justin Too <justin@doubleotoo.com>
# Date: September 11, 2015
#------------------------------------------------------------------------------

from spack import *

class Doxygen(Package):
    """Doxygen is the de facto standard tool for generating documentation
    from annotated C++ sources, but it also supports other popular programming
    languages such as C, Objective-C, C#, PHP, Java, Python, IDL (Corba,
    Microsoft, and UNO/OpenOffice flavors), Fortran, VHDL, Tcl, and to some extent D..
    """
    homepage = "http://www.stack.nl/~dimitri/doxygen/"
    url      = "http://ftp.stack.nl/pub/users/dimitri/doxygen-1.8.10.src.tar.gz"

    version('1.8.10', '79767ccd986f12a0f949015efb5f058f')

    depends_on("cmake@2.8.12:")

    def install(self, spec, prefix):
        cmake('.', *std_cmake_args)

        make()
        make("install")
