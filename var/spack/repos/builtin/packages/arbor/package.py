# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Arbor(CMakePackage, CudaPackage):
    """Arbor is a high-performance library for computational neuroscience
    simulations."""

    homepage = 'https://arbor-sim.org'
    git      = 'https://github.com/arbor-sim/arbor.git'
    url      = 'https://github.com/arbor-sim/arbor/releases/download/v0.6/arbor-v0.6-full.tar.gz'
    maintainers = ['bcumming', 'brenthuisman', 'haampie', 'schmitts']

    version('master', branch='master', submodules=True)
    version('0.6', sha256='4cd333b18effc8833428ddc0b99e7dc976804771bc85da90034c272c7019e1e8', url='https://github.com/arbor-sim/arbor/releases/download/v0.6/arbor-v0.6-full.tar.gz')
    version('0.5.2', sha256='290e2ad8ca8050db1791cabb6b431e7c0409c305af31b559e397e26b300a115d', url='https://github.com/arbor-sim/arbor/releases/download/v0.5.2/arbor-v0.5.2-full.tar.gz')
    version('0.5', sha256='d0c8a4c7f97565d7c30493c66249be794d1dc424de266fc79cecbbf0e313df59', url='https://github.com/arbor-sim/arbor/releases/download/v0.5/arbor-v0.5-full.tar.gz')

    variant('assertions', default=False, description='Enable arb_assert() assertions in code.')
    variant('doc', default=False, description='Build documentation.')
    variant('mpi', default=False, description='Enable MPI support')
    variant('neuroml', default=True, description='Build NeuroML support library.')
    variant('python', default=True, description='Enable Python frontend support')
    variant('vectorize', default=False, description='Enable vectorization of computational kernels')

    # https://docs.arbor-sim.org/en/latest/install/build_install.html?highlight=requirements#compilers
    conflicts('%gcc@:8.3')
    conflicts('%clang@:7')
    # Cray compiler v9.2 and later is Clang-based.
    conflicts('%cce@:9.1')
    conflicts('%intel')

    depends_on('cmake@3.12:', type='build')

    # misc dependencies
    depends_on('fmt@7.1:', when='@0.5.3:')  # required by the modcc compiler
    depends_on('nlohmann-json')
    depends_on('cuda@10:', when='+cuda')
    depends_on('libxml2', when='+neuroml')

    # mpi
    depends_on('mpi', when='+mpi')
    depends_on('py-mpi4py', when='+mpi+python', type=('build', 'run'))

    # python (bindings)
    extends('python', when='+python')
    depends_on('python@3.6:', when="+python", type=('build', 'run'))
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    with when('+python'):
        depends_on('py-pybind11@2.6:', type=('build', 'run'))
        depends_on('py-pybind11@2.8.1:', when='@0.5.3:', type=('build', 'run'))

    # sphinx based documentation
    depends_on('python@3.6:', when="+doc", type='build')
    depends_on('py-sphinx', when="+doc", type='build')
    depends_on('py-svgwrite', when='+doc', type='build')

    @property
    def build_targets(self):
        return ['all', 'html'] if '+doc' in self.spec else ['all']

    def cmake_args(self):
        args = [
            self.define_from_variant('ARB_WITH_ASSERTIONS', 'assertions'),
            self.define_from_variant('ARB_WITH_MPI', 'mpi'),
            self.define_from_variant('ARB_WITH_NEUROML', 'neuroml'),
            self.define_from_variant('ARB_WITH_PYTHON', 'python'),
            self.define_from_variant('ARB_VECTORIZE', 'vectorize'),
        ]

        if '+cuda' in self.spec:
            args.append('-DARB_GPU=cuda')

        # query spack for the architecture-specific compiler flags set by its wrapper
        args.append('-DARB_ARCH=none')
        opt_flags = self.spec.target.optimization_flags(
            self.spec.compiler.name,
            self.spec.compiler.version)
        args.append('-DARB_CXX_FLAGS_TARGET=' + opt_flags)

        return args
