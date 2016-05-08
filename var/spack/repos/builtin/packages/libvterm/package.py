from spack import *

class Libvterm(Package):
    """An abstract library implementation of a terminal emulator"""
    homepage = "http://www.leonerd.org.uk/code/libvterm/"
    url      = "http://www.leonerd.org.uk/code/libvterm/libvterm-0+bzr681.tar.gz"

    version('681', '7a4325a7350b7092245c04e8ee185ac3')

    def install(self, spec, prefix):
        make()
        make("install", "PREFIX=" + prefix)
