import os
from spack import *
import os

class Qt(Package):
    """Qt is a comprehensive cross-platform C++ application framework."""
    homepage = "http://qt.io"
    list_url   = 'http://download.qt-project.org/official_releases/qt/'
    list_depth = 2

    version('5.4.0', 'e8654e4b37dd98039ba20da7a53877e6',
            url='http://download.qt-project.org/official_releases/qt/5.4/5.4.0/single/qt-everywhere-opensource-src-5.4.0.tar.gz')
    version('5.3.2', 'febb001129927a70174467ecb508a682',
            url='http://download.qt.io/archive/qt/5.3/5.3.2/single/qt-everywhere-opensource-src-5.3.2.tar.gz')

    version('5.2.1', 'a78408c887c04c34ce615da690e0b4c8',
            url='http://download.qt.io/archive/qt/5.2/5.2.1/single/qt-everywhere-opensource-src-5.2.1.tar.gz')
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

    # Webkit
    # depends_on("gperf")
    # depends_on("flex")
    # depends_on("bison")
    # depends_on("ruby")
    # depends_on("icu4c")

    # OpenGL hardware acceleration
    depends_on("mesa")
    depends_on("libxcb")


    def setup_dependent_environment(self, module, spec, dep_spec):
        """Dependencies of Qt find it using the QTDIR environment variable."""
        os.environ['QTDIR'] = self.prefix


    def patch(self):
        if self.spec.satisfies('@4'):
            qmake_conf      = 'mkspecs/common/g++-base.conf'
            qmake_unix_conf = 'mkspecs/common/g++-unix.conf'
        elif self.spec.satisfies('@5'):
            qmake_conf      = 'qtbase/mkspecs/common/g++-base.conf'
            qmake_unix_conf = 'qtbase/mkspecs/common/g++-unix.conf'
        else:
            return

        # Fix qmake compilers in the default mkspec
        filter_file(r'^QMAKE_COMPILER *=.*$',  'QMAKE_COMPILER = cc', qmake_conf)
        filter_file(r'^QMAKE_CC *=.*$',        'QMAKE_CC = cc',       qmake_conf)
        filter_file(r'^QMAKE_CXX *=.*$',       'QMAKE_CXX = c++',     qmake_conf)
        filter_file(r'^QMAKE_LFLAGS_NOUNDEF *\+?=.*$',  'QMAKE_LFLAGS_NOUNDEF =', qmake_unix_conf)


    @property
    def common_config_args(self):
        return [
            '-prefix', self.prefix,
            '-v',
            '-opensource',
            '-opengl',
            "-release",
            '-shared',
            '-confirm-license',
            '-openssl-linked',
            '-dbus-linked',
            '-optimized-qmake',
            '-no-openvg',
            '-no-pch',
            # NIS is deprecated in more recent glibc
            "-no-nis"]
    # Don't disable all the database drivers, but should
    # really get them into spack at some point.


    @when('@4')
    def configure(self):
        configure('-fast',
                  '-no-webkit',
                  *self.common_config_args)


    @when('@5')
    def configure(self):
        configure('-no-eglfs',
                  '-no-directfb',
                  '-qt-xcb',
                  # If someone wants to get a webkit build working, be my guest!
                  '-skip', 'qtwebkit',
                  *self.common_config_args)


    def install(self, spec, prefix):
        self.configure()
        make()
        make("install")
