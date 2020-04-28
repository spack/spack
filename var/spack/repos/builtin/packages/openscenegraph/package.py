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
    variant('ffmpeg', default=False, description='Builds ffmpeg plugin for audio encoding/decoding')

    depends_on('cmake@2.8.7:', type='build')
    depends_on('qt+opengl')
    depends_on('qt@4:', when='@3.2:')
    depends_on('qt@:4', when='@:3.1')
    depends_on('libxinerama')
    depends_on('libxrandr')
    depends_on('jasper')
    depends_on('zlib')

    depends_on('ffmpeg+avresample', when='+ffmpeg')
    # https://github.com/openscenegraph/OpenSceneGraph/issues/167
    depends_on('ffmpeg@:2', when='@:3.4.0+ffmpeg')

    patch('glibc-jasper.patch', when='@3.4%gcc')

    def cmake_args(self):
        spec = self.spec

        shared_status = 'ON' if '+shared' in spec else 'OFF'
        opengl_profile = 'GL{0}'.format(spec['gl'].version.up_to(1))

        args = [
            # Variant Options #
            '-DDYNAMIC_OPENSCENEGRAPH={0}'.format(shared_status),
            '-DDYNAMIC_OPENTHREADS={0}'.format(shared_status),
            '-DOPENGL_PROFILE={0}'.format(opengl_profile),

            # General Options #
            '-DBUILD_OSG_APPLICATIONS=OFF',
            '-DOSG_NOTIFY_DISABLED=ON',
            '-DLIB_POSTFIX=',
            '-DCMAKE_RELWITHDEBINFO_POSTFIX=',
            '-DCMAKE_MINSIZEREL_POSTFIX='
        ]

        if spec.satisfies('~ffmpeg'):
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

        return args
