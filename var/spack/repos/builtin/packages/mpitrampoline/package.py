# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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
    version('4.0.1', sha256='b1622b408c76bd6ac7ccd30b66066d8b08dd0a67596988b215ee9870ba0a9811')
    version('4.0.0', sha256='6fcd9683059da79e530bedf61ec27ce98567b6b39575272fd2fa637fe3df3edd')
    version('3.8.0', sha256='493e9a383012a43d77d142775c332928aa3302a1f591ee06b88d5f9145281e00')
    version('3.7.0', sha256='f2d018dd7bbed4ed177b49fcbfef9cabdd5f2c614257ce4c599ab7214130b097')
    version('3.6.0', sha256='cc2c0630243aae43e6502ebe52f1cfe7fecbcf2930e9fe0f69b77c0bbb3f08ff')
    version('3.5.1', sha256='5e6439b2cceb69c53f2fee8bec1b913c527166a03207e8739dab7d6b41d47747')
    version('3.5.0', sha256='e7497bfa5902cd62fdd40aff1de654c782218cf07f776ba2a8b78815044d2df3')
    version('3.4.1', sha256='03728045f1d19b2ed3eeb10e9c86b2db8891d3eedd5db7ce81a647c88b2cd98f')
    version('3.4.0', sha256='9dd4d7434a2df4ac3807d07ffe46f00316a6f7f8e6393213b900d4ceb24403bb')
    version('3.3.1', sha256='53ce6db1f6197330883243543401d85ebab25d204687ea699f4767f6bd9890aa')
    version('3.3.0', sha256='0a4b465fdf0a7329bf998c1adb47dfaed0b1a85d41ff305fa3205f2d2a6f39ba')
    version('3.2.0', sha256='88efa3b9b116c89db0c819306caef85b2a97dd4596531856187d6bf59eb4a8b1')
    version('3.1.0', sha256='588adba1c84b2a828b054be5e12a4acac820744ab18762c830e9c606f36b50c3')
    version('3.0.0', sha256='4a2a1f1d5108e27e4d7f2b46a1dce3c9211f65ac67d0a3281812beade45901d8')
    version('2.8.1', sha256='97a1f0c4e06d3b5a92034ebdb334e711b2859e4648a7f728b98abd8e8c96edd7')
    version('2.8.0', sha256='bc2a075ced19e5f7ea547060e284887bdbb0761d34d1adb6f16d2e9e096a7d38')
    version('2.7.0', sha256='b188657e41b240bba663ce5b3d7b73377a27a64edcc1e0aaa7c924cf00e30b42')
    version('2.6.0', sha256='5425085f4b8772990b28a643b7dfc7ac37a399ee35ffa3d6113a06e5b508dfac')
    version('2.5.0', sha256='26423749a6a45324062cbe82eb6934236b0c8ea17f9d5b594ed0c15ea8d0dbad')
    version('2.4.0', sha256='e08785cf5b43c9913d890be44f6e7a551a83f34f389f6db9136db2379697fadd')
    version('2.3.0', sha256='4559acb13d34b9a052752a9e0f928d31da54bfa7b05f31585bf6a66fadaceca4')
    version('2.2.0', sha256='fa213a7ac03b4c54d5c9281192fb604747d4b5be4ce9b54b4c740f3da7a6aaea')
    version('2.1.0', sha256='8794c07772ecc6d979ecf475653ae571a593d01ef2df51ccbc63c9f9d9c67856')
    version('2.0.0', sha256='50d4483f73ea4a79a9b6d025d3abba42f76809cba3165367f4810fb8798264b6')
    version('1.1.0', sha256='67fdb710d1ca49487593a9c023e94aa8ff0bec56de6005d1a437fca40833def9')
    version('1.0.1', sha256='4ce91b99fb6d2dab481b5e477b6b6a0709add48cf0f287afbbb440fdf3232500')

    variant('shared', default=True,
            description='Build a shared version of the library')

    provides("mpi @3.1")

    def cmake_args(self):
        return [self.define_from_variant('BUILD_SHARED_LIBS', 'shared')]

    @property
    def headers(self):
        return HeaderList(find(self.prefix.include, 'mpi.h'))

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters
        # MPItrampoline does not support the (outdated) C++ API
        assert 'cxx' not in query_parameters
        libraries = ['libmpitrampoline']
        return find_libraries(libraries, root=self.prefix.lib, shared=True)

    def setup_build_environment(self, env):
        fflags = ['-fcray-pointer']
        if self.spec.satisfies('%apple-clang@11:'):
            fflags.append('-fallow-argument-mismatch')
        if self.spec.satisfies('%clang@11:'):
            fflags.append('-fallow-argument-mismatch')
        if self.spec.satisfies('%gcc@10:'):
            fflags.append('-fallow-argument-mismatch')
        env.set('FFLAGS', ' '.join(fflags))

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
        # Use the Spack compiler wrappers under MPI
        env.set('MPITRAMPOLINE_CC', spack_cc)
        env.set('MPITRAMPOLINE_CXX', spack_cxx)
        env.set('MPITRAMPOLINE_FC', spack_fc)

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.mpicc = join_path(self.prefix.bin, 'mpicc')
        self.spec.mpicxx = join_path(self.prefix.bin, 'mpicxx')
        self.spec.mpif77 = join_path(self.prefix.bin, 'mpifc')
        self.spec.mpifc = join_path(self.prefix.bin, 'mpifc')
