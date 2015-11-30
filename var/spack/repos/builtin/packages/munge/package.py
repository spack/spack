from spack import *
import os

class Munge(Package):
    """ MUNGE Uid 'N' Gid Emporium """
    homepage = "https://code.google.com/p/munge/"
    url      = "https://github.com/dun/munge/releases/download/munge-0.5.11/munge-0.5.11.tar.bz2"

    version('0.5.11', 'bd8fca8d5f4c1fcbef1816482d49ee01', url='https://github.com/dun/munge/releases/download/munge-0.5.11/munge-0.5.11.tar.bz2')

    depends_on('openssl')
    depends_on('libgcrypt')

    def install(self, spec, prefix):
        os.makedirs(os.path.join(prefix, "lib/systemd/system"))
        configure("--prefix=%s" % prefix)

        make()
        make("install")

