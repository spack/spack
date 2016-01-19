from spack import *

class Libarchive(Package):
    """libarchive: C library and command-line tools for reading and
       writing tar, cpio, zip, ISO, and other archive formats."""
    homepage = "http://www.libarchive.org"
    url      = "http://www.libarchive.org/downloads/libarchive-3.1.2.tar.gz"

    version('3.1.2', 'efad5a503f66329bb9d2f4308b5de98a')
    version('3.1.1', '1f3d883daf7161a0065e42a15bbf168f')
    version('3.1.0', '095a287bb1fd687ab50c85955692bf3a')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
