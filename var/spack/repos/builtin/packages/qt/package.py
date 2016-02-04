from spack import *
import os

class Qt(Package):
    """Qt is a comprehensive cross-platform C++ application framework."""
    homepage = 'http://qt.io'
    url      = 'http://download.qt.io/archive/qt/5.5/5.5.1/single/qt-everywhere-opensource-src-5.5.1.tar.gz'

    version('5.5.1',  '59f0216819152b77536cf660b015d784')
    version('5.4.0',  'e8654e4b37dd98039ba20da7a53877e6')
    version('5.3.2',  'febb001129927a70174467ecb508a682')
    version('5.2.1',  'a78408c887c04c34ce615da690e0b4c8')
    version('4.8.6',  '2edbe4d6c2eff33ef91732602f3518eb')
    version('3.3.8b', '9f05b4125cfe477cc52c9742c3c09009')

    # Add patch for compile issues with qt3 found with use in the OpenSpeedShop project
    variant('krellpatch', default=False, description="build with openspeedshop based patch.")
    variant('gtk', default=False, description="build with gtkplus.")

    patch('qt3krell.patch', when='@3.3.8b+krellpatch')

    # Use system openssl for security.
    #depends_on("openssl")

    depends_on("glib")
    depends_on("gtkplus", when='+gtk')
    depends_on("libxml2")
    depends_on("zlib")
    depends_on("dbus", when='@4:')
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
    depends_on("mesa", when='@4:')
    depends_on("libxcb")


    def url_for_version(self, version):
        url = "http://download.qt.io/archive/qt/"

        if version >= Version('5'):
            url += "%s/%s/single/qt-everywhere-opensource-src-%s.tar.gz" % \
                    (version.up_to(2), version, version)
        elif version >= Version('4.8'):
            url += "%s/%s/qt-everywhere-opensource-src-%s.tar.gz" % \
                    (version.up_to(2), version, version)
        elif version >= Version('4.6'):
            url += "%s/qt-everywhere-opensource-src-%s.tar.gz" % \
                    (version.up_to(2), version)
        elif version >= Version('4.0'):
            url += "%s/qt-x11-opensource-src-%s.tar.gz" % \
                    (version.up_to(2), version)
        elif version >= Version('3'):
            url += "%s/qt-x11-free-%s.tar.gz" % \
                    (version.up_to(1), version)
        elif version >= Version('2.1'):
            url += "%s/qt-x11-%s.tar.gz" % \
                    (version.up_to(1), version)
        else:
            url += "%s/qt-%s.tar.gz" % \
                    (version.up_to(1), version)

        return url


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

    @when('@3')
    def configure(self):
        configure('-prefix', self.prefix,
                  '-v',
                  '-thread',
                  '-shared',
                  '-release',
                  '-fast'
                  )

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
