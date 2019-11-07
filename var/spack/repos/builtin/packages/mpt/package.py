# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mpt(Package):
    """HPE MPI is HPE's implementation of
    the Message Passing Interface (MPI) standard.

    Note: HPE MPI is proprietry software. Spack will search your
    current directory for the download file. Alternatively, add this file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://buy.hpe.com/us/en/software/high-performance-computing-software/hpe-message-passing-interface-mpi/p/1010144155"

    provides('mpi')
    provides('mpi@:3.1', when='@3:')
    provides('mpi@:1.3', when='@1:')

    filter_compiler_wrappers(
        'mpicc', 'mpicxx', 'mpif77', 'mpif90', 'mpif77', 'mpif08',
        relative_root='bin'
    )

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters
        libraries = ['libmpi']

        if 'cxx' in query_parameters:
            libraries = ['libmpicxx'] + libraries

        return find_libraries(
            libraries, root=self.prefix, shared=True, recursive=True
        )

    def setup_dependent_build_environment(self, spack_env, run_env, 
                                          dependent_spec):
        spack_env.set('MPICC',  self.prefix.bin.mpicc)
        spack_env.set('MPICXX', self.prefix.bin.mpicxx)
        spack_env.set('MPIF77', self.prefix.bin.mpif77)
        spack_env.set('MPIF90', self.prefix.bin.mpifc)
        spack_env.set('MPICC_CC', spack_cc)
        spack_env.set('MPICXX_CXX', spack_cxx)
        spack_env.set('MPIF90_F90', spack_fc)

    def setup_dependent_package(self, module, dependent_spec):
        if 'platform=cray' in self.spec:
            self.spec.mpicc = spack_cc
            self.spec.mpicxx = spack_cxx
            self.spec.mpifc = spack_fc
            self.spec.mpif77 = spack_f77
        else:
            self.spec.mpicc = self.prefix.bin.mpicc
            self.spec.mpicxx = self.prefix.bin.mpicxx
            self.spec.mpifc = self.prefix.bin.mpifc
            self.spec.mpif77 = self.prefix.bin.mpif77

    @property
    def fetcher(self):
        msg = """This package is a placeholder for HPE MPI, a
        system-provided, proprietary MPI implementation.

        Add to your packages.yaml (changing the /opt/ path to match
        where HPE MPI is actually installed):

        packages:
          mpt:
            paths:
              mpt@2.20: /opt/
            buildable: False

        """
        raise InstallError(msg)
