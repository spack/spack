from spack import *

class Pixman(Package):
    """The Pixman package contains a library that provides low-level
       pixel manipulation features such as image compositing and
       trapezoid rasterization."""
    homepage = "http://www.pixman.org"
    url      = "http://cairographics.org/releases/pixman-0.32.6.tar.gz"

    version('0.32.6', '3a30859719a41bd0f5cccffbfefdd4c2')

    depends_on("libpng")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--disable-gtk")
        make()
        make("install")
