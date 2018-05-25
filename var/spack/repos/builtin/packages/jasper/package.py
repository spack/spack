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


class Jasper(CMakePackage):
    """Library for manipulating JPEG-2000 images"""

    homepage = "https://www.ece.uvic.ca/~frodo/jasper/"
    url      = "https://www.ece.uvic.ca/~frodo/jasper/software/jasper-2.0.14.tar.gz"
    list_url = homepage

    version('2.0.14',  '23561b51da8eb5d0dc85b91eff3d9a7f')

    variant('jpeg',   default=True,  description='Enable the use of the JPEG library')
    variant('opengl', default=False, description='Enable the use of the OpenGL and GLUT libraries')
    variant('shared', default=True,  description='Enable the building of shared libraries')

    depends_on('cmake@2.8.11:', type='build')
    depends_on('jpeg', when='+jpeg')
    depends_on('gl', when='+opengl')

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DJAS_ENABLE_DOC=false'
        ]

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
