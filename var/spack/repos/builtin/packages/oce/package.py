from spack import *
import platform, sys

class Oce(Package):
    """
    Open CASCADE Community Edition:
    patches/improvements/experiments contributed by users over the official Open CASCADE library.
    """
    homepage = "https://github.com/tpaviot/oce"
    url      = "https://github.com/tpaviot/oce/archive/OCE-0.17.tar.gz"

    version('0.17.1', '36c67b87093c675698b483454258af91')
    version('0.17'  , 'f1a89395c4b0d199bea3db62b85f818d')
    version('0.16.1', '4d591b240c9293e879f50d86a0cb2bb3')
    version('0.16'  , '7a4b4df5a104d75a537e25e7dd387eca')

    variant('tbb', default=True, description='Build with Intel Threading Building Blocks')

    depends_on('cmake@2.8:')
    depends_on('tbb', when='+tbb')

    # There is a bug in OCE which appears with Clang (version?) or GCC 6.0
    # and has to do with compiler optimization, see
    # https://github.com/tpaviot/oce/issues/576
    # http://tracker.dev.opencascade.org/view.php?id=26042
    # https://github.com/tpaviot/oce/issues/605
    # https://github.com/tpaviot/oce/commit/61cb965b9ffeca419005bc15e635e67589c421dd.patch
    patch('null.patch',when='@0.16:0.17.1')


    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)
        options.extend([
            '-DOCE_INSTALL_PREFIX=%s' % prefix,
            '-DOCE_BUILD_SHARED_LIB:BOOL=ON',
            '-DCMAKE_BUILD_TYPE:STRING=Release',
            '-DOCE_DATAEXCHANGE:BOOL=ON',
            '-DOCE_DISABLE_X11:BOOL=ON',
            '-DOCE_DRAW:BOOL=OFF',
            '-DOCE_MODEL:BOOL=ON',
            '-DOCE_MULTITHREAD_LIBRARY:STRING=%s' % ('TBB' if '+tbb' in spec else 'NONE'),
            '-DOCE_OCAF:BOOL=ON',
            '-DOCE_USE_TCL_TEST_FRAMEWORK:BOOL=OFF',
            '-DOCE_VISUALISATION:BOOL=OFF',
            '-DOCE_WITH_FREEIMAGE:BOOL=OFF',
            '-DOCE_WITH_GL2PS:BOOL=OFF',
            '-DOCE_WITH_OPENCL:BOOL=OFF'
        ])

        if platform.system() == 'Darwin':
            options.extend([
                '-DOCE_OSX_USE_COCOA:BOOL=ON',
            ])

        cmake('.', *options)

        make("install/strip")

        # OCE tests build is brocken at least on Darwin.
        # Unit tests are linked against libTKernel.10.dylib isntead of /full/path/libTKernel.10.dylib
        # see https://github.com/tpaviot/oce/issues/612
        # make("test")

        # The shared libraries are not installed correctly on Darwin; correct this
        if (sys.platform == 'darwin'):
            fix_darwin_install_name(prefix.lib)
