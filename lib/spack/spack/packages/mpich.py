from spack import *

class Mpich(Package):
    homepage = "http://www.mpich.org"
    url      = "http://www.mpich.org/static/downloads/3.0.4/mpich-3.0.4.tar.gz"
    md5      = "9c5d5d4fe1e17dd12153f40bc5b6dbc0"

    list_url   = "http://www.mpich.org/static/downloads/"
    list_depth = 2

    def install(self, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
