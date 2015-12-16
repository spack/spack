from spack import *

class Fontconfig(Package):
    """Fontconfig customizing font access"""
    homepage = "http://www.freedesktop.org/wiki/Software/fontconfig/"
    url      = "http://www.freedesktop.org/software/fontconfig/release/fontconfig-2.11.1.tar.gz"

    version('2.11.1' , 'e75e303b4f7756c2b16203a57ac87eba')

    depends_on('freetype')
    depends_on('libxml2')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix, "--enable-libxml2")

        make()
        make("install")
