# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SpectrumMpi(Package):
    """IBM MPI implementation from Spectrum MPI."""

    homepage = "http://www-03.ibm.com/systems/spectrum-computing/products/mpi"

    provides('mpi')

    def install(self, spec, prefix):
        raise InstallError('IBM MPI is not installable; it is vendor supplied')

    def setup_dependent_package(self, module, dependent_spec):
        # get the compiler names
        if '%xl' in dependent_spec or '%xl_r' in dependent_spec:
            self.spec.mpicc = join_path(self.prefix.bin, 'mpixlc')
            self.spec.mpicxx = join_path(self.prefix.bin, 'mpixlC')
            self.spec.mpif77 = join_path(self.prefix.bin, 'mpixlf')
            self.spec.mpifc = join_path(self.prefix.bin, 'mpixlf')
        elif '%pgi' in dependent_spec:
            self.spec.mpicc = join_path(self.prefix.bin, 'mpipgicc')
            self.spec.mpicxx = join_path(self.prefix.bin, 'mpipgic++')
            self.spec.mpif77 = join_path(self.prefix.bin, 'mpipgifort')
            self.spec.mpifc = join_path(self.prefix.bin, 'mpipgifort')
        else:
            self.spec.mpicc = join_path(self.prefix.bin, 'mpicc')
            self.spec.mpicxx = join_path(self.prefix.bin, 'mpicxx')
            self.spec.mpif77 = join_path(self.prefix.bin, 'mpif77')
            self.spec.mpifc = join_path(self.prefix.bin, 'mpif90')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        if '%xl' in dependent_spec or '%xl_r' in dependent_spec:
            spack_env.set('MPICC', join_path(self.prefix.bin, 'mpixlc'))
            spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpixlC'))
            spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpixlf'))
            spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpixlf'))
        elif '%pgi' in dependent_spec:
            spack_env.set('MPICC', join_path(self.prefix.bin, 'mpipgicc'))
            spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpipgic++'))
            spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpipgifort'))
            spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpipgifort'))
        else:
            spack_env.set('MPICC', join_path(self.prefix.bin, 'mpicc'))
            spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpic++'))
            spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpif77'))
            spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpif90'))

        spack_env.set('OMPI_CC', spack_cc)
        spack_env.set('OMPI_CXX', spack_cxx)
        spack_env.set('OMPI_FC', spack_fc)
        spack_env.set('OMPI_F77', spack_f77)

        spack_env.prepend_path('LD_LIBRARY_PATH', self.prefix.lib)
