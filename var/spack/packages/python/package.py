from spack import *


class Python(Package):
    """The Python programming language."""
    homepage = "http://www.python.org"
    url      = "http://www.python.org/ftp/python/2.7.8/Python-2.7.8.tar.xz"

    extendable = True

    version('2.7.8', 'd235bdfa75b8396942e360a70487ee00')

    depends_on("openssl")
    depends_on("bzip2")
    depends_on("readline")
    depends_on("ncurses")
    depends_on("sqlite")

    def install(self, spec, prefix):
        # Need this to allow python build to find the Python installation.
        env['PYTHONHOME'] = prefix

        # Rest of install is pretty standard.
        configure("--prefix=%s" % prefix,
                  "--with-threads",
                  "--enable-shared")
        make()
        make("install")
