##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class PyShapely(PythonPackage):
    """Manipulation and analysis of geometric objects in the Cartesian plane.
    """

    homepage = "https://github.com/Toblerity/Shapely"
    url      = "https://pypi.io/packages/source/S/Shapely/Shapely-1.6.4.tar.gz"

    version('1.6.4', '7581ef2d0fb346f9ed157f3efc75f6a4')

    depends_on('python@2.6.0:2.8,3.4.0:', type=('build', 'run'))
    depends_on('py-setuptools',     type='build')
    depends_on('py-cython@0.19:',   type='build')
    depends_on('py-numpy@1.4.1:',   type=('build', 'run'))
    depends_on('geos@3.3:')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('GEOS_CONFIG', self.spec['geos'].prefix)
        spack_env.prepend_path('LD_LIBRARY_PATH', self.spec['geos'].prefix.lib)
