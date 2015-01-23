from spack import *

class Qt(Package):
    """Qt is a comprehensive cross-platform C++ application framework."""
    homepage = "http://qt.io"

    version('4.8.6', '2edbe4d6c2eff33ef91732602f3518eb',
            url="http://download.qt-project.org/official_releases/qt/4.8/4.8.6/qt-everywhere-opensource-src-4.8.6.tar.gz")

    # Use system openssl for security.
    #depends_on("openssl")

    depends_on("glib")
    depends_on("gtkplus")
    depends_on("libxml2")
    depends_on("zlib")
    depends_on("dbus")
    depends_on("libtiff")
    depends_on("libpng")
    depends_on("libmng")
    depends_on("jpeg")

    def patch(self):
        # Fix qmake compilers in the default mkspec
        qmake_conf = 'mkspecs/common/g++-base.conf'
        filter_file(r'^QMAKE_CC *=.*$',  'QMAKE_CC = cc', qmake_conf)
        filter_file(r'^QMAKE_CXX *=.*$', 'QMAKE_CXX = c++', qmake_conf)


    def install(self, spec, prefix):
        configure('-v',
                  '-confirm-license',
                  '-opensource',
                  '-prefix', prefix,
                  '-openssl-linked',
                  '-dbus-linked',
                  '-fast',
                  '-optimized-qmake',
                  '-no-pch',
# phonon required for py-pyqt4
#                  '-no-phonon',
#                  '-no-phonon-backend',
                  '-no-openvg')
        make()
        make("install")
