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
import platform


class Vecgeom(CMakePackage):
    """The vectorized geometry library for particle-detector simulation
    (toolkits)."""

    homepage = "https://gitlab.cern.ch/VecGeom/VecGeom"
    url = "https://gitlab.cern.ch/api/v4/projects/VecGeom%2FVecGeom/repository/archive.tar.gz?sha=v0.3.rc"

    version('0.3.rc', 'c1f5d620f655f3c0610a44e7735203b5')

    depends_on('cmake@3.5:', type='build')

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
