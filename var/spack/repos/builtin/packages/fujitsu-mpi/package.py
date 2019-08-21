# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FujitsuMpi(Package):
    """Fujitsu MPI implementation only for Fujitsu compiler."""

    version('3.0')

    provides('mpi@3.1:')

    def install(self, spec, prefix):
        raise InstallError(
            'Fujitsu MPI is not installable; it is vendor supplied')

    def setup_dependent_package(self, module, dependent_spec):
        if '%fj' in dependent_spec:
            self.spec.mpicc = join_path(self.prefix.bin, 'mpifcc')
            self.spec.mpicxx = join_path(self.prefix.bin, 'mpiFCC')
            self.spec.mpif77 = join_path(self.prefix.bin, 'mpifrt')
            self.spec.mpifc = join_path(self.prefix.bin, 'mpifrt')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        if '%fj' in dependent_spec:
            spack_env.set('MPICC', join_path(self.prefix.bin, 'mpifcc'))
            spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpiFCC'))
            spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpifrt'))
            spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpifrt'))

        spack_env.set('OMPI_CC', spack_cc)
        spack_env.set('OMPI_CXX', spack_cxx)
        spack_env.set('OMPI_FC', spack_fc)
        spack_env.set('OMPI_F77', spack_f77)

        spack_env.prepend_path('LD_LIBRARY_PATH', self.prefix.lib)
