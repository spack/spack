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
import platform


class Vecgeom(CMakePackage):
    """The vectorized geometry library for particle-detector simulation
    (toolkits)."""

    homepage = "https://gitlab.cern.ch/VecGeom/VecGeom"

    version('0.3.rc', git='https://gitlab.cern.ch/VecGeom/VecGeom.git',
            tag='v0.3.rc')

    variant('debug', default=False, description='Build debug version')

    depends_on('cmake@3.5:', type='build')

    def build_type(self):
        spec = self.spec
        if '+debug' in spec:
            return 'Debug'
        else:
            return 'Release'

    def cmake_args(self):
        options = [
            '-DBACKEND=Scalar',
            '-DGEANT4=OFF',
            '-DUSOLIDS=ON',
            '-DUSOLIDS_VECGEOM=ON'
        ]

        arch = platform.machine()
        if arch == 'x86_64':
            options.append('-DVECGEOM_VECTOR=sse4.2')
        else:
            options.append('-DVECGEOM_VECTOR=' + arch)
        return options
