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
import os


class IntelMpiExternal(Package):
    """Helper package for Intel MPI to configure as external package.
       When Intel MPI is installed as standalone package outside Parallel
       Studio then Spack couldn't find the path. This package helps to find
       necessary paths and libraries. """

    homepage = "https://software.intel.com/en-us/intel-mpi-library"
    url = "https://software.intel.com/en-us/intel-mpi-library"

    version('develop', '0123456789abcdef0123456789abcdef')

    provides('mpi')

    @property
    def bin_dir(self):
        if os.path.isdir(self.prefix.bin):
            return self.prefix.bin
        elif os.path.isdir(self.prefix.bin64):
            return self.prefix.bin64
        else:
            raise RuntimeError('No bin directory found in IntelMpiExternal')

    def install(self, spec, prefix):
        raise RuntimeError('IntelMpiExternal package is not installable')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('I_MPI_CC', spack_cc)
        spack_env.set('I_MPI_CXX', spack_cxx)
        spack_env.set('I_MPI_F77', spack_fc)
        spack_env.set('I_MPI_F90', spack_f77)
        spack_env.set('I_MPI_FC', spack_fc)

    def setup_dependent_package(self, module, dep_spec):
        # Intel comes with 2 different flavors of MPI wrappers:
        #
        # * mpiicc, mpiicpc, and mpifort are hardcoded to wrap around
        #   the Intel compilers.
        # * mpicc, mpicxx, mpif90, and mpif77 allow you to set which
        #   compilers to wrap using I_MPI_CC and friends. By default,
        #   wraps around the GCC compilers.
        #
        # In theory, these should be equivalent as long as I_MPI_CC
        # and friends are set to point to the Intel compilers, but in
        # practice, mpicc fails to compile some applications while
        # mpiicc works.
        bindir = self.bin_dir

        if self.compiler.name == 'intel':
            self.spec.mpicc  = bindir.mpiicc
            self.spec.mpicxx = bindir.mpiicpc
            self.spec.mpifc  = bindir.mpiifort
            self.spec.mpif77 = bindir.mpiifort
        else:
            self.spec.mpicc  = bindir.mpicc
            self.spec.mpicxx = bindir.mpicxx
            self.spec.mpifc  = bindir.mpif90
            self.spec.mpif77 = bindir.mpif77
