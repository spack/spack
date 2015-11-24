from spack import *
from spack.util.environment import *

class Cityhash(Package):
    homepage = "https://github.com/google/cityhash"
    url      = "https://github.com/google/cityhash"

    version('2013-07-31', git='https://github.com/google/cityhash.git', commit='8af9b8c2b889d80c22d6bc26ba0df1afb79a30db')
    version('master', branch='master', git='https://github.com/google/cityhash.git')

    def install(self, spec, prefix):
        configure('--enable-sse4.2', '--prefix=%s' % prefix)

        make()
        make("install")

