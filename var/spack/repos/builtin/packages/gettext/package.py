from spack import *

class Gettext(Package):
    """TODO"""
    homepage = "https://www.gnu.org/software/gettext/"
    url      = "http://ftp.gnu.org/pub/gnu/gettext/gettext-0.19.6.tar.xz"

    version('0.19.6', '69d79254ee3b41df23f41c2f4fd720d9')

    depends_on("libffi")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
