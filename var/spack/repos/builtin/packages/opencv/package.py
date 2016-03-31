from spack import *


class Opencv(Package):
    """
    OpenCV is released under a BSD license and hence it's free for both academic and commercial use. It has C++, C,
    Python and Java interfaces and supports Windows, Linux, Mac OS, iOS and Android. OpenCV was designed for
    computational efficiency and with a strong focus on real-time applications. Written in optimized C/C++, the library
    can take advantage of multi-core processing. Enabled with OpenCL, it can take advantage of the hardware
    acceleration of the underlying heterogeneous compute platform. Adopted all around the world, OpenCV has more than
    47 thousand people of user community and estimated number of downloads exceeding 9 million. Usage ranges from
    interactive art, to mines inspection, stitching maps on the web or through advanced robotics.
    """
    homepage = 'http://opencv.org/'
    url = 'https://github.com/Itseez/opencv/archive/3.1.0.tar.gz'

    version('3.1.0', '70e1dd07f0aa06606f1bc0e3fa15abd3')

    variant('shared', default=True, description='Enables the build of shared libraries')
    variant('debug', default=False, description='Builds a debug version of the libraries')

    variant('eigen', default=True, description='Activates support for eigen')
    variant('ipp', default=True, description='Activates support for IPP')

    depends_on('zlib')
    depends_on('libpng')
    depends_on('libjpeg-turbo')
    depends_on('libtiff')

    depends_on('python')
    depends_on('py-numpy')

    depends_on('eigen', when='+eigen')

    # FIXME : GUI extensions missing
    # FIXME : CUDA extensions still missing

    def install(self, spec, prefix):
        cmake_options = []
        cmake_options.extend(std_cmake_args)

        cmake_options.extend(['-DCMAKE_BUILD_TYPE:STRING=%s' % ('Debug' if '+debug' in spec else 'Release'),
                              '-DBUILD_SHARED_LIBS:BOOL=%s' % ('ON' if '+shared' in spec else 'OFF'),
                              '-DENABLE_PRECOMPILED_HEADERS:BOOL=OFF',
                              '-DWITH_IPP:BOOL=%s' % ('ON' if '+ipp' in spec else 'OFF')])

        with working_dir('spack_build', create=True):
            which('cmake')('..', *cmake_options)
            make('VERBOSE=1')
            make("install")
