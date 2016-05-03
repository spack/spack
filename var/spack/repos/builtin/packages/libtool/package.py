from spack import *

class Libtool(Package):
    """libtool -- library building part of autotools"""
    homepage = "https://www.gnu.org/software/libtool/"
    url      = "http://ftpmirror.gnu.org/libtool/libtool-2.4.6.tar.gz"

    version('2.4.6' , 'addf44b646ddb4e3919805aa88fa7c5e')
    version('2.4.2' , 'd2f3b7d4627e69e13514a40e72a24d50')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
