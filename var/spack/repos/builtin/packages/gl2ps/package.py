##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Gl2ps(CMakePackage):
    """GL2PS is a C library providing high quality vector output for any
    OpenGL application."""

    homepage = "http://www.geuz.org/gl2ps/"
    url      = "http://geuz.org/gl2ps/src/gl2ps-1.3.9.tgz"

    version('1.3.9', '377b2bcad62d528e7096e76358f41140')

    variant('png',  default=True, description='Enable PNG support')
    variant('zlib', default=True, description='Enable compression using ZLIB')

    depends_on('cmake@2.4:', type='build')

    # TODO: Add missing dependencies on OpenGL/Mesa and LaTeX

    # X11 libraries:
    depends_on('libice')
    depends_on('libsm')
    depends_on('libxau')
    depends_on('libxdamage')
    depends_on('libxdmcp')
    depends_on('libxext')
    depends_on('libxfixes')
    depends_on('libxi')
    depends_on('libxmu')
    depends_on('libxt')
    depends_on('libxxf86vm')
    depends_on('libxcb')
    depends_on('libdrm')
    depends_on('expat')

    depends_on('libpng', when='+png')
    depends_on('zlib',   when='+zlib')

    def variant_to_bool(self, variant):
        return 'ON' if variant in self.spec else 'OFF'

    def cmake_args(self):
        return [
            '-DENABLE_PNG={0}'.format(self.variant_to_bool('+png')),
            '-DENABLE_ZLIB={0}'.format(self.variant_to_bool('+zlib')),
        ]
