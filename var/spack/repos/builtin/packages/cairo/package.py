from spack import *

class Cairo(Package):
    """Cairo is a 2D graphics library with support for multiple output devices."""
    homepage = "http://cairographics.org"
    url      = "http://cairographics.org/releases/cairo-1.14.0.tar.xz"

    version('1.14.0', 'fc3a5edeba703f906f2241b394f0cced')

    depends_on("libpng")
    depends_on("glib")
    depends_on("pixman")
    depends_on("fontconfig@2.10.91:") # Require newer version of fontconfig.

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--enable-tee")
        make()
        make("install")
