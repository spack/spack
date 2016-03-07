from spack import *

class Libsigsegv(Package):
    """GNU libsigsegv is a library for handling page faults in user mode."""
    homepage = "https://www.gnu.org/software/libsigsegv/"
    url      = "ftp://ftp.gnu.org/gnu/libsigsegv/libsigsegv-2.10.tar.gz"

    version('2.10', '7f96fb1f65b3b8cbc1582fb7be774f0f')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix,
                  '--enable-shared')

        make()
        make("install")
