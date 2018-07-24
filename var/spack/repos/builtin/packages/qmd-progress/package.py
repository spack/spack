##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
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


class QmdProgress(CMakePackage):
    """PROGRESS: Parallel, Rapid O(N) and Graph-based Recursive Electronic
    Structure Solver.
    This library is focused on the development of general solvers that are
    commonly used in quantum chemistry packages."""

    homepage = "https://github.com/lanl/qmd-progress"
    url      = "https://github.com/lanl/qmd-progress/tarball/v1.1.0"
    git      = "https://github.com/lanl/qmd-progress.git"

    version('develop', branch='master')
    version('1.1.0', 'dda155134f0925629bf116e562c0a4bd')
    version('1.0.0', 'c950bead2719a47a78864e3376ba143e')

    variant('graphlib', default=False, description='Build with Metis Suppport')
    variant('mpi', default=True, description='Build with MPI Support')
    variant('shared', default=True, description='Build shared libs')

    depends_on('bml')
    depends_on('mpi', when='+mpi')
    depends_on('metis', when='+graphlib')

    def cmake_args(self):
        spec = self.spec
        args = ['-DCMAKE_Fortran_FLAGS=-ffree-line-length-none']
        if '+shared' in spec:
            args.append('-DBUILD_SHARED_LIBS=ON')
        else:
            args.append('-DBUILD_SHARED_LIBS=OFF')
        if '+mpi' in spec:
            args.append('-DPROGRESS_MPI=yes')
            args.append('-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc)
            args.append('-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx)
            args.append('-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc)
        else:
            args.append('-DPROGRESS_MPI=no')
        if '+graphlib' in spec:
            args.append('-DPROGRESS_GRAPHLIB=yes')
        else:
            args.append('-DPROGRESS_GRAPHLIB=no')

        return args
