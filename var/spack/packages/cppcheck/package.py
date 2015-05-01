from spack import *

class Cppcheck(Package):
    """A tool for static C/C++ code analysis."""
    homepage = "http://cppcheck.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/cppcheck/cppcheck/1.68/cppcheck-1.68.tar.bz2"

    version('1.68', 'c015195f5d61a542f350269030150708')

    def install(self, spec, prefix):
        # cppcheck does not have a configure script
        make()
        # manually install the final cppcheck binary
        mkdirp(prefix.bin)
        install('cppcheck', prefix.bin)
