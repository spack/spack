# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gunrock(CMakePackage, CudaPackage):
    """High-Performance Graph Primitives on GPUs"""

    homepage = "https://gunrock.github.io/docs/"
    git      = "https://github.com/gunrock/gunrock.git"

    version('master',   submodules=True)
    version('1.1',      submodules=True, tag='v1.1')
    version('1.0',      submodules=True, tag='v1.0')
    version('0.5.1',    submodules=True, tag='v0.5.1')
    version('0.5',      submodules=True, tag='v0.5')
    version('0.4',      submodules=True, tag='v0.4')
    version('0.3.1',    submodules=True, tag='v0.3.1')
    version('0.3',      submodules=True, tag='v0.3')
    version('0.2',      submodules=True, tag='v0.2')
    version('0.1',      submodules=True, tag='v0.1')

    variant('lib',                  default=True,  description='Build main gunrock library')
    variant('shared_libs',          default=True,  description='Turn off to build for static libraries')
    variant('tests',                default=False, description='Build tests')
    variant('mgpu_tests',           default=False, description='Builds Gunrock applications and enables the ctest framework for single GPU implementations')
    variant('cuda_verbose_ptxas',   default=False, description='Enable verbose output from the PTXAS assembler')
    variant('google_tests',         default=False, description='Build unit tests using googletest')
    variant('code_coverage',        default=False, description="run code coverage on Gunrock's source code")
    variant('all_applications',     default=True,  description='Build all applications')

    depends_on('google-tests', when='+google_tests')
    depends_on('lcov', when='+code_coverage')

    def cmake_args(self):
        spec = self.spec
        args = []
        args.extend([
                    '-DGUNROCK_BUILD_LIB={0}'.format(
                        'ON' if '+lib' in spec else 'OFF'),
                    '-DGUNROCK_BUILD_SHARED_LIBS={0}'.format(
                        'ON' if '+shared_libs' in spec else 'OFF'),
                    '-DGUNROCK_BUILD_TESTS={0}'.format(
                        'ON' if '+tests' in spec else 'OFF'),
                    '-DGUNROCK_BUILD_MGPU_TESTS={0}'.format(
                        'ON' if '+mgpu_tests' in spec else 'OFF'),
#                    '-DGUNROCK_BUILD_GENCODE_SM={0}'.format(
#                        'ON' if '+cuda' in spec else 'OFF'),
                    '-DCUDA_VERBOSE_PTXAS={0}'.format(
                        'ON' if '+cuda_verbose_ptxas' in spec else 'OFF'),
                    '-DGUNROCK_GOOGLE_TESTS={0}'.format(
                        'ON' if '+google_tests' in spec else 'OFF'),
                    '-DGUNROCK_CODE_COVERAGE={0}'.format(
                        'ON' if '+code_coverage' in spec else 'OFF'),
                    '-DGUNROCK_BUILD_APPLICATIONS={0}'.format(
                        'ON' if '+all_applications' in spec else 'OFF'),
])

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            install_tree('bin', prefix.bin)
            install_tree('lib', prefix.lib)
