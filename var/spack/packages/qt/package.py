from spack import *

class Qt(Package):
    """Qt is a comprehensive cross-platform C++ application framework."""
    homepage = "http://qt.io"

    version('4.8.6', '2edbe4d6c2eff33ef91732602f3518eb',
            url="http://download.qt-project.org/official_releases/qt/4.8/4.8.6/qt-everywhere-opensource-src-4.8.6.tar.gz")

    # depends_on("zlib")

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        configure("--prefix=%s" % prefix)

        # FIXME: Add logic to build and install here
        make()
        make("install")
