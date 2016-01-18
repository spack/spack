from spack import *

class Libsodium(Package):
    """Sodium is a modern, easy-to-use software library for encryption,
    decryption, signatures, password hashing and more."""
    homepage = "https://download.libsodium.org/doc/"
    url      = "https://download.libsodium.org/libsodium/releases/libsodium-1.0.3.tar.gz"

    version('1.0.3', 'b3bcc98e34d3250f55ae196822307fab')
    version('1.0.2', 'dc40eb23e293448c6fc908757738003f')
    version('1.0.1', '9a221b49fba7281ceaaf5e278d0f4430')
    version('1.0.0', '3093dabe4e038d09f0d150cef064b2f7')
    version('0.7.1', 'c224fe3923d1dcfe418c65c8a7246316')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
