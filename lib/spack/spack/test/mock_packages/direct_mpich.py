from spack import *

class DirectMpich(Package):
    homepage = "http://www.example.com"
    url      = "http://www.example.com/direct_mpich-1.0.tar.gz"

    versions = { 1.0 : 'foobarbaz' }

    depends_on('mpich')

    def install(self, spec, prefix):
        pass
