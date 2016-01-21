from spack import *

class Tar(Package):
    """GNU Tar provides the ability to create tar archives, as well as various other kinds of manipulation."""
    homepage = "https://www.gnu.org/software/tar/"
    url      = "http://ftp.gnu.org/gnu/tar/tar-1.28.tar.gz"

    version('1.28', '6ea3dbea1f2b0409b234048e021a9fd7')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make('install')
