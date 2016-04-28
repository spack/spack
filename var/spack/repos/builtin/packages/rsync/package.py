from spack import *

class Rsync(Package):
    """rsync is an open source utility that provides fast incremental file transfer."""
    homepage = "https://rsync.samba.org"
    url      = "https://download.samba.org/pub/rsync/rsync-3.1.1.tar.gz"

    version('3.1.2', '0f758d7e000c0f7f7d3792610fad70cb')
    version('3.1.1', '43bd6676f0b404326eee2d63be3cdcfe')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
