from spack import *

class Python(Package):
    """The Python programming language."""
    homepage = "http://www.python.org"
    url      = "http://www.python.org/ftp/python/2.7.8/Python-2.7.8.tar.xz"

    version('2.7.8', 'd235bdfa75b8396942e360a70487ee00')

    depends_on("openssl")
    depends_on("sqlite")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
