# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Openscenegraph(CMakePackage):
    """OpenSceneGraph is an open source, high performance 3D graphics toolkit
       that's used in a variety of visual simulation applications."""

    homepage = "http://www.openscenegraph.org"
    git_url  = "https://github.com/openscenegraph/OpenSceneGraph.git"

    version('3.6.5', git=git_url, tag='OpenSceneGraph-3.6.5')
    version('3.6.4', git=git_url, tag='OpenSceneGraph-3.6.4')
    version('3.4.1', git=git_url, tag='OpenSceneGraph-3.4.1')
    version('3.4.0', git=git_url, tag='OpenSceneGraph-3.4.0')
    version('3.2.3', git=git_url, tag='OpenSceneGraph-3.2.3')
    version('3.1.5', git=git_url, tag='OpenSceneGraph-3.1.5')

    variant('shared', default=True, description='Builds a shared version of the library')

    depends_on('cmake@2.8.7:', type='build')
    depends_on('qt+opengl')
    depends_on('qt@4:', when='@3.2:')
    depends_on('qt@:4', when='@:3.1')
    # TODO: Since 'ffmpeg' constantly changes its API and OSG must change in response,
    # the version of the dependency here matters greatly on the version and patch of
    # the release of OSG that's being used.
    depends_on('ffmpeg@1:2+avresample')
    depends_on('zlib')
    depends_on('libxinerama')
    depends_on('libxrandr')

    patch('glibc-jasper.patch', when='@3.4.0:3.4.999%gcc')

    def cmake_args(self):
        spec = self.spec

        shared_status = 'ON' if '+shared' in spec else 'OFF'
        opengl_profile = 'GL{0}'.format(spec['gl'].version.up_to(1))

        args = [
            # Library Options #
            '-DZLIB_INCLUDE_DIR={0}'.format(spec['zlib'].prefix.include),
            '-DZLIB_LIBRARY={0}/libz.{1}'.format(spec['zlib'].prefix.lib,
                                                 dso_suffix),
            '-DFFMPEG_ROOT={0}'.format(spec['ffmpeg'].prefix),
            # Variant Options #
            '-DDYNAMIC_OPENSCENEGRAPH={0}'.format(shared_status),
            '-DDYNAMIC_OPENTHREADS={0}'.format(shared_status),
            '-DOPENGL_PROFILE={0}'.format(opengl_profile),
            # General Options #
            '-DBUILD_OSG_APPLICATIONS=OFF',
            '-DOSG_NOTIFY_DISABLED=ON',
            '-DLIB_POSTFIX=',
            '-DCMAKE_RELWITHDEBINFO_POSTFIX=',
        ]
        if spec.satisfies('@:3.2'):
            args.extend([
                '-DZLIB_INCLUDE_DIR={0}'.format(spec['zlib'].prefix.include),
                '-DZLIB_LIBRARY={0}/libz.{1}'.format(spec['zlib'].prefix.lib,
                                                     dso_suffix),
            ])

        # NOTE: Specifying only the root seems to be sufficient, and specifying
        # the locations explicity causes OSG to be buggy.
        for ffmpeg_lib in ['libavcodec', 'libavformat', 'libavutil']:
            args.extend([
                '-DFFMPEG_{0}_INCLUDE_DIRS='.format(ffmpeg_lib.upper()),
                '-DFFMPEG_{0}_LIBRARIES='.format(ffmpeg_lib.upper()),
            ])

        # NOTE: This is necessary in order to allow OpenSceneGraph to compile
        # despite containing a number of implicit bool to int conversions.
        if spec.satisfies('%gcc'):
            args.extend([
                '-DCMAKE_C_FLAGS=-fpermissive',
                '-DCMAKE_CXX_FLAGS=-fpermissive',
            ])

        if spec.satisfies('@3.4:'):
            args.extend(['-DBUILD_OSG_FRAMEWORKS=OFF'])

        return args
