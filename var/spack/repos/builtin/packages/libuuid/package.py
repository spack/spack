from spack import *

class Libuuid(Package):
    """Portable uuid C library"""
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://sourceforge.net/projects/libuuid/"
    url      = "http://downloads.sourceforge.net/project/libuuid/libuuid-1.0.3.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Flibuuid%2F&ts=1433881396&use_mirror=iweb"

    version('1.0.3', 'd44d866d06286c08ba0846aba1086d68')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        # FIXME: Add logic to build and install here
        make()
        make("install")
