# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Openscenegraph(CMakePackage):
    """OpenSceneGraph is an open source, high performance 3D graphics toolkit
       that's used in a variety of visual simulation applications."""

    homepage = "http://www.openscenegraph.org"
    url      = "https://github.com/openscenegraph/OpenSceneGraph/archive/OpenSceneGraph-3.6.4.tar.gz"

    version('3.6.4', sha256='81394d1b484c631028b85d21c5535280c21bbd911cb058e8746c87e93e7b9d33')
    version('3.2.3', sha256='a1ecc6524197024834e1277916922b32f30246cb583e27ed19bf3bf889534362')
    version('3.1.5', sha256='dddecf2b33302076712100af59b880e7647bc595a9a7cc99186e98d6e0eaeb5c')

    variant('shared', default=True, description='Builds a shared version of the library')

    depends_on('cmake@2.8.7:', type='build')
    depends_on('qt@4:')
    depends_on('zlib')

    def cmake_args(self):
        spec = self.spec

        shared_status = 'ON' if '+shared' in spec else 'OFF'

        args = [
            '-DDYNAMIC_OPENSCENEGRAPH={0}'.format(shared_status),
            '-DDYNAMIC_OPENTHREADS={0}'.format(shared_status),
            '-DZLIB_INCLUDE_DIR={0}'.format(spec['zlib'].prefix.include),
            '-DZLIB_LIBRARY={0}/libz.{1}'.format(spec['zlib'].prefix.lib,
                                                 dso_suffix),
            '-DBUILD_OSG_APPLICATIONS=OFF',
            '-DOSG_NOTIFY_DISABLED=ON',
            '-DLIB_POSTFIX=',
        ]

        # NOTE: This is necessary in order to allow OpenSceneGraph to compile
        # despite containing a number of implicit bool to int conversions.
        if spec.satisfies('%gcc'):
            args.extend([
                '-DCMAKE_C_FLAGS=-fpermissive',
                '-DCMAKE_CXX_FLAGS=-fpermissive',
            ])

        return args
