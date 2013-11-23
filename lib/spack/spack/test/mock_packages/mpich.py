from spack import *

class Mpich(Package):
    homepage = "http://www.mpich.org"
    url      = "http://www.mpich.org/static/downloads/3.0.4/mpich-3.0.4.tar.gz"
    md5      = "9c5d5d4fe1e17dd12153f40bc5b6dbc0"

    list_url   = "http://www.mpich.org/static/downloads/"
    list_depth = 2

    versions = '1.0.3, 1.3.2p1, 1.4.1p1, 3.0.4, 3.1b1'

    provides('mpi')

    def install(self, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
