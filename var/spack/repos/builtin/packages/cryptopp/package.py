import glob
from spack import *

class Cryptopp(Package):
    """Crypto++ is an open-source C++ library of cryptographic schemes. The
       library supports a number of different cryptography algorithms, including
       authenticated encryption schemes (GCM, CCM), hash functions (SHA-1, SHA2),
       public-key encryption (RSA, DSA), and a few obsolete/historical encryption
       algorithms (MD5, Panama)."""

    homepage = "http://www.cryptopp.com/"
    url      = "http://www.cryptopp.com/cryptopp563.zip"

    version('5.6.3', '3c5b70e2ec98b7a24988734446242d07')
    version('5.6.2', '7ed022585698df48e65ce9218f6c6a67')

    def install(self, spec, prefix):
        make()

        mkdirp(prefix.include)
        for hfile in glob.glob('*.h*'):
            install(hfile, prefix.include)

        mkdirp(prefix.lib)
        install('libcryptopp.a', prefix.lib)

    def url_for_version(self, version):
        version_tuple = tuple(v for v in iter(version))
        version_string = reduce(lambda vs, nv: vs + str(nv), version_tuple, "")

        return "%scryptopp%s.zip" % (Cryptopp.homepage, version_string)
