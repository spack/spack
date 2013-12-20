from spack import *

class Mpich(Package):
    homepage   = "http://www.mpich.org"
    url        = "http://www.mpich.org/static/downloads/3.0.4/mpich-3.0.4.tar.gz"
    list_url   = "http://www.mpich.org/static/downloads/"
    list_depth = 2

    versions = { '3.0.4' : '9c5d5d4fe1e17dd12153f40bc5b6dbc0',
                 '3.0.3' : 'foobarbaz',
                 '3.0.2' : 'foobarbaz',
                 '3.0.1' : 'foobarbaz',
                 '3.0'   : 'foobarbaz' }

    provides('mpi@:3', when='@3:')
    provides('mpi@:1', when='@1:')

    def install(self, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
