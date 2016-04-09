from spack import *

class Openscenegraph(Package):
    """TODO(JRC)"""

    homepage = "http://www.openscenegraph.org"
    url      = "http://trac.openscenegraph.org/downloads/developer_releases/OpenSceneGraph-3.4.0.zip"

    version('3.4.0', 'a5e762c64373a46932e444f6f7332496')
    version('3.2.3', '02ffdad7744c747d8fad0d7babb58427')

    variant('debug', default=False, description='Builds a debug version of the library')
    variant('shared', default=True, description='Builds a shared version of the library')

    # TODO: Make this a build dependency once build dependencies are supported
    # (see: https://github.com/LLNL/spack/pull/378).
    depends_on('cmake@2.8.7:')
    depends_on('qt@4:')
    depends_on('zlib')

    def install(self, spec, prefix):
        cmake_args = [
            '-DCMAKE_BUILD_TYPE=%s' % ( 'Release' if '+debug' in spec else 'Debug' ),
            '-DDYNAMIC_OPENSCENEGRAPH=%s' % ( 'ON' if '+shared' in spec else 'OFF' ),
            '-DDYNAMIC_OPENTHREADS=%s' % ( 'ON' if '+shared' in spec else 'OFF' ),
        ]

        mkdirp('build')
        cd('build')

        cmake('..',
            '-DCMAKE_INSTALL_PREFIX=%s' % prefix,
            '-DCMAKE_C_COMPILER=%s' % self.compilers.cc,
            '-DCMAKE_CXX_COMPILER=%s' % self.compilers.cxx,
            '-DZLIB_INCLUDE_DIR=%s' % spec['zlib'].prefix.include,
            '-DZLIB_LIBRARY=%s/libz.so' % spec['zlib'].prefix.lib,
            '-DBUILD_OSG_APPLICATIONS=OFF',
            '-DFFMPEG_LIBAVCODEC_INCLUDE_DIRS=""',
            '-DFFMPEG_LIBAVFORMAT_INCLUDE_DIRS=""',
            '-DFFMPEG_LIBAVUTIL_INCLUDE_DIRS=""',
            '-DOSG_NOTIFY_DISABLED=ON',
            '-DLIB_POSTFIX=""',
            *cmake_args)

        make()
        make('install')
