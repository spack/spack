from spack import *

class Curl(Package):
    """cURL is an open source command line tool and library for
    transferring data with URL syntax"""

    homepage = "http://curl.haxx.se"
    url      = "http://curl.haxx.se/download/curl-7.46.0.tar.bz2"

    version('7.46.0', '9979f989a2a9930d10f1b3deeabc2148')
    version('7.45.0', '62c1a352b28558f25ba6209214beadc8')
    version('7.44.0', '6b952ca00e5473b16a11f05f06aa8dae')
    version('7.43.0', '11bddbb452a8b766b932f859aaeeed39')
    version('7.42.1', '296945012ce647b94083ed427c1877a8')

    depends_on("openssl")
    depends_on("zlib")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix,
                  '--with-zlib=%s' % spec['zlib'].prefix,
                  '--with-ssl=%s' % spec['openssl'].prefix)

        make()
        make("install")
