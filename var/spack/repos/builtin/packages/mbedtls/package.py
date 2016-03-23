from spack import *

class Mbedtls(Package):
    """
    mbed TLS (formerly known as PolarSSL) makes it trivially easy for developers to include cryptographic and SSL/TLS capabilities in their (embedded) products, facilitating this functionality with a minimal coding footprint.
    """
    homepage = "https://tls.mbed.org"
    url      = "https://github.com/ARMmbed/mbedtls/archive/mbedtls-2.2.1.tar.gz"

    version('2.2.1' , '73a38f96898d6d03e32f55dd9f9a67be')
    version('2.2.0' , 'eaf4586c1ef93ae872e606b6c1203942')
    version('2.1.4' , '40cdf67b6c6d92c9cbcfd552d39ea3ae')
    version('2.1.3' , '7eb4cf1dfa68578a2c8dbd0b6fa752dd')
    version('1.3.16', '4144d7320c691f721aeb9e67a1bc38e0')

    depends_on('cmake')

    def install(self, spec, prefix):
        cmake = which('cmake')
        cmake('.', *std_cmake_args)

        make()
        make("install")
