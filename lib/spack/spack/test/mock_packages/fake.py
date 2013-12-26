from spack import *

class Fake(Package):
    homepage = "http://www.fake-spack-example.org"
    url      = "http://www.fake-spack-example.org/downloads/fake-1.0.tar.gz"
    versions = { '1.0' : 'foobarbaz' }

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
