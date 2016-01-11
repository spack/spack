from spack import *

class Szip(Package):
    """Szip is an implementation of the extended-Rice lossless compression algorithm.
    It provides lossless compression of scientific data, and is provided with HDF
    software products."""

    homepage = "https://www.hdfgroup.org/doc_resource/SZIP/"
    url      = "http://www.hdfgroup.org/ftp/lib-external/szip/2.1/src/szip-2.1.tar.gz"

    version('2.1', '902f831bcefb69c6b635374424acbead')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix,
                  '--enable-production',
                  '--enable-shared',
                  '--enable-static',
                  '--enable-encoding')

        make()
        make("install")
