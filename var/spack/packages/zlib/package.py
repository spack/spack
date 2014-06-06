from spack import *

class Zlib(Package):
    """zlib is designed to be a free, general-purpose, legally unencumbered --
       that is, not covered by any patents -- lossless data-compression library for
       use on virtually any computer hardware and operating system.
    """

    homepage = "http://zlib.net"
    url      = "http://zlib.net/zlib-1.2.8.tar.gz"

    versions = { '1.2.8' : '44d667c142d7cda120332623eab69f40', }

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
