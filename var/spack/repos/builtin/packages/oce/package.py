from spack import *
import platform

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
    version('0.15'  , '7ec541a1c350ca8a684f74980e48801c')

    depends_on('cmake@2.8:')

    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)
        options.extend([
            '-DOCE_INSTALL_PREFIX=%s' % prefix,
            '-DOCE_BUILD_SHARED_LIB:BOOL=ON',
            '-DOCE_BUILD_TYPE:STRING=Release',
            '-DOCE_DATAEXCHANGE:BOOL=ON',
            '-DOCE_DISABLE_X11:BOOL=ON',
            '-DOCE_DRAW:BOOL=OFF',
            '-DOCE_MODEL:BOOL=ON',
            '-DOCE_MULTITHREAD_LIBRARY:STRING=NONE', # FIXME: add tbb
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
