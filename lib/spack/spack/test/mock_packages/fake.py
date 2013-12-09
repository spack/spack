from spack import *

class Fake(Package):
    homepage = "http://www.fake-spack-example.org"
    url      = "http://www.fake-spack-example.org/downloads/fake-1.0.tar.gz"
    md5      = "foobarbaz"

    versions = '1.0'

    def install(self, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
