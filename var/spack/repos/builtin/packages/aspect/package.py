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


class Aspect(CMakePackage):
    """Parallel, extendible finite element code to simulate convection in the
    Earth's mantle and elsewhere."""

    homepage = "https://aspect.geodynamics.org"
    url      = "https://github.com/geodynamics/aspect/releases/download/v2.0.0/aspect-2.0.0.tar.gz"
    git      = "https://github.com/geodynamics/aspect.git"

    maintainers = ['tjhei']

    version('develop', branch='master')
    version('2.0.0', 'dfecc571fb221f28a0800034cd29c95c')

    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))
    variant('gui', default=False, description='Enable the deal.II parameter GUI')
    variant('fpe', default=False, description='Enable floating point exception checks')

    depends_on('dealii+p4est+trilinos+mpi')
    depends_on('dealii-parameter-gui', when='+gui')

    def cmake_args(self):
        return [
            '-DASPECT_USE_FP_EXCEPTIONS=%s' %
            ('ON' if '+fpe' in self.spec else 'OFF')
        ]

    def setup_environment(self, spack_env, run_env):
        run_env.set('Aspect_DIR', self.prefix)
