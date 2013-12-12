from spack import *

class Mpich(Package):
    """MPICH is a high performance and widely portable implementation of
       the Message Passing Interface (MPI) standard."""

    homepage = "http://www.mpich.org"
    url      = "http://www.mpich.org/static/downloads/3.0.4/mpich-3.0.4.tar.gz"
    md5      = "9c5d5d4fe1e17dd12153f40bc5b6dbc0"

    list_url   = "http://www.mpich.org/static/downloads/"
    list_depth = 2

    versions = ['3.0.4', '3.0.3', '3.0.2', '3.0.1', '3.0']

    provides('mpi@:3', when='@3:')
    provides('mpi@:1', when='@1:')

    def install(self, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
