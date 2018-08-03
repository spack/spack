##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Jasper(Package):
    """Library for manipulating JPEG-2000 images"""

    homepage = "https://www.ece.uvic.ca/~frodo/jasper/"
    url      = "https://www.ece.uvic.ca/~frodo/jasper/software/jasper-2.0.14.tar.gz"
    list_url = homepage

    version('2.0.14',  '23561b51da8eb5d0dc85b91eff3d9a7f',
            url="https://www.ece.uvic.ca/~frodo/jasper/software/jasper-2.0.14.tar.gz")
    version('1.900.1', 'a342b2b4495b3e1394e161eb5d85d754',
            url="https://www.ece.uvic.ca/~frodo/jasper/software/jasper-1.900.1.zip")

    variant('jpeg',   default=True,  description='Enable the use of the JPEG library')
    variant('opengl', default=False, description='Enable the use of the OpenGL and GLUT libraries')
    variant('shared', default=True,  description='Enable the building of shared libraries')
    variant('build_type', default='Release', description='CMake build type', values=('Debug', 'Release'))

    depends_on('cmake@2.8.11:', type='build', when='@2:')
    depends_on('jpeg', when='+jpeg')
    depends_on('gl', when='+opengl')

    # Fixes a bug where an assertion fails when certain JPEG-2000
    # files with an alpha channel are processed.
    # See: https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=469786
    patch('fix_alpha_channel_assert_fail.patch', when='@1.900.1')

    def cmake_args(self):
        spec = self.spec
        args = std_cmake_args
        args.append('-DJAS_ENABLE_DOC=false')

        if '+jpeg' in spec:
            args.append('-DJAS_ENABLE_LIBJPEG=true')
        else:
            args.append('-DJAS_ENABLE_LIBJPEG=false')

        if '+opengl' in spec:
            args.append('-DJAS_ENABLE_OPENGL=true')
        else:
            args.append('-DJAS_ENABLE_OPENGL=false')

        if '+shared' in spec:
            args.append('-DJAS_ENABLE_SHARED=true')
        else:
            args.append('-DJAS_ENABLE_SHARED=false')

        return args

    def configure_args(self):
        spec = self.spec
        args = [
            '--prefix={0}'.format(self.prefix)
        ]

        if '+jpeg' in spec:
            args.append('--enable-libjpeg')
        else:
            args.append('--disable-libjpeg')

        if '+opengl' in spec:
            args.append('--enable-opengl')
        else:
            args.append('--disable-opengl')

        if '+shared' in spec:
            args.append('--enable-shared')
        else:
            args.append('--disable-shared')

        if 'build_type=Debug' in spec:
            args.append('--enable-debug')
        else:
            args.append('--disable-debug')

        return args

    @when('@2:')
    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *self.cmake_args())
            make()
            if self.run_tests:
                make('test')
            make('install')

    @when('@:1')
    def install(self, spec, prefix):
        configure(*self.configure_args())
        make()
        if self.run_tests:
            make('check')
        make('install')
        if self.run_tests:
            make('installcheck')
