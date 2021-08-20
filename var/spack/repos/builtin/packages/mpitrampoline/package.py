# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mpitrampoline(CMakePackage):
    """MPItrampoline: A forwarding MPI implementation that can use any other
    MPI implementation via an MPI ABI."""

    homepage = "https://github.com/eschnett/MPItrampoline"
    url      = "https://github.com/eschnett/MPItrampoline/archive/v1.0.1.tar.gz"
    git      = "https://github.com/eschnett/MPItrampoline.git"

    maintainers = ['eschnett']

    version('develop', branch='main')
    version('1.0.1', sha256='4ce91b99fb6d2dab481b5e477b6b6a0709add48cf0f287afbbb440fdf3232500')

    variant('shared', default=True,
            description='Build a shared version of the library')

    provides("mpi @3.1")

    def cmake_args(self):
        return [self.define_from_variant('BUILD_SHARED_LIBS', 'shared')]

    def setup_run_environment(self, env):
        # Because MPI implementations provide compilers, they have to add to
        # their run environments the code to make the compilers available.
        env.set('MPITRAMPOLINE_CC', self.compiler.cc_names[0])
        env.set('MPITRAMPOLINE_CXX', self.compiler.cxx_names[0])
        env.set('MPITRAMPOLINE_FC', self.compiler.fc_names[0])
        env.set('MPICC', join_path(self.prefix.bin, 'mpicc'))
        env.set('MPICXX', join_path(self.prefix.bin, 'mpicxx'))
        env.set('MPIF77', join_path(self.prefix.bin, 'mpifc'))
        env.set('MPIF90', join_path(self.prefix.bin, 'mpifc'))

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_run_environment(env)

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.mpicc = join_path(self.prefix.bin, 'mpicc')
        self.spec.mpicxx = join_path(self.prefix.bin, 'mpicxx')
        self.spec.mpif77 = join_path(self.prefix.bin, 'mpifc')
        self.spec.mpifc = join_path(self.prefix.bin, 'mpifc')
