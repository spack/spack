##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class Clamr(CMakePackage):
    """The CLAMR code is a cell-based adaptive mesh refinement (AMR)
    mini-app developed as a testbed for hybrid algorithm development
    using MPI and OpenCL GPU code.
    """

    homepage = "https://github.com/lanl/CLAMR"
    git      = "https://github.com/lanl/CLAMR.git"
    tags     = ['proxy-app']

    version('master')

    variant(
        'graphics', default='opengl',
        values=('opengl', 'mpe', 'none'),
        description='Build with specified graphics support')
    variant(
        'precision', default='mixed',
        values=('single', 'mixed', 'full'),
        description='single, mixed, or full double precision values')

    depends_on('cmake@3.1:')
    depends_on('mpi')
    depends_on('mpe', when='graphics=mpe')

    def cmake_args(self):
        spec = self.spec
        cmake_args = []
        if 'graphics=none' in spec:
            cmake_args.append('-DGRAPHICS_TYPE=None')
        elif 'graphics=mpe' in spec:
            cmake_args.append('-DGRAPHICS_TYPE=MPE')
        else:
            cmake_args.append('-DGRAPHICS_TYPE=OpenGL')

        if 'precision=full' in spec:
            cmake_args.append('-DPRECISION_TYPE=full_precision')
        elif 'precision=single' in spec:
            cmake_args.append('-DPRECISION_TYPE=minimum_precision')
        else:
            cmake_args.append('-DPRECISION_TYPE=mixed_precision')

        # if MIC, then -DMIC_NATIVE=yes
        return cmake_args

    def install(self, spec, prefix):
        install('README', prefix)
        install('LICENSE', prefix)
        install_tree('docs', join_path(prefix, 'docs'))
        install_tree('tests', join_path(prefix, 'tests'))
        with working_dir(self.build_directory):
            make('install')
