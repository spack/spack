from spack import *

class Coreutils(Package):
    """The GNU Core Utilities are the basic file, shell and text
       manipulation utilities of the GNU operating system.  These are
       the core utilities which are expected to exist on every
       operating system.
    """
    homepage = "http://www.gnu.org/software/coreutils/"
    url      = "http://ftp.gnu.org/gnu/coreutils/coreutils-8.23.tar.xz"

    version('8.23', 'abed135279f87ad6762ce57ff6d89c41')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
