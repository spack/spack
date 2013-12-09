from spack import *

class Mpich2(Package):
    homepage = "http://www.mpich.org"
    url      = "http://www.mpich.org/static/downloads/1.5/mpich2-1.5.tar.gz"
    md5      = "9c5d5d4fe1e17dd12153f40bc5b6dbc0"

    list_url   = "http://www.mpich.org/static/downloads/"
    list_depth = 2

    versions = '1.5, 1.4, 1.3, 1.2, 1.1, 1.0'

    provides('mpi@:2.0')
    provides('mpi@:2.1', when='@1.1:')
    provides('mpi@:2.2', when='@1.2:')

    def install(self, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
