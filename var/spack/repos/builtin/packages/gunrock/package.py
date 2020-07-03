# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gunrock(CMakePackage, CudaPackage):
    """High-Performance Graph Primitives on GPUs"""

    homepage = "https://gunrock.github.io/docs/"
    git      = "https://github.com/gunrock/gunrock.git"

    # tagged versions are broken. See
    # https://github.com/gunrock/gunrock/issues/777
    # Hence, prefer a specific commit.
    version('master',   submodules=True)
    version('2020-06-15',   submodules=True, commit='81f58d628463561969dafe65868e72251562e806', preferred=True)
    version('1.1',      submodules=True, tag='v1.1')
    version('1.0',      submodules=True, tag='v1.0')
    version('0.5.1',    submodules=True, tag='v0.5.1')
    version('0.5',      submodules=True, tag='v0.5')
    version('0.4',      submodules=True, tag='v0.4')
    version('0.3.1',    submodules=True, tag='v0.3.1')
    version('0.3',      submodules=True, tag='v0.3')
    version('0.2',      submodules=True, tag='v0.2')
    version('0.1',      submodules=True, tag='v0.1')

    variant('cuda', default=True, description="Build with Cuda support")

    variant('lib',                  default=True,  description='Build main gunrock library')
    variant('shared_libs',          default=True,  description='Turn off to build for static libraries')
    variant('tests',                default=True,  description='Build functional tests / examples')
    variant('mgpu_tests',           default=False, description='Builds Gunrock applications and enables the ctest framework for single GPU implementations')
    variant('cuda_verbose_ptxas',   default=False, description='Enable verbose output from the PTXAS assembler')
    variant('google_tests',         default=False, description='Build unit tests using googletest')
    variant('code_coverage',        default=False, description="run code coverage on Gunrock's source code")
    variant('all_applications',     default=True,  description='Build all applications')
    # apps
    variant('app_bc',       default=False, description='Only build BC primitive')
    variant('app_bfs',      default=False, description='Only build BFS primitive')
    variant('app_cc',       default=False, description='Only build CC primitive')
    variant('app_pr',       default=False, description='Only build PR primitive')
    variant('app_sssp',     default=False, description='Only build SSSP primitive')
    variant('app_dobfs',    default=False, description='Only build DOBFS primitive')
    variant('app_hits',     default=False, description='Only build HITS primitive')
    variant('app_salsa',    default=False, description='Only build SALSA primitive')
    variant('app_mst',      default=False, description='Only build MST primitive')
    variant('app_wtf',      default=False, description='Only build WTF primitive')
    variant('app_topk',     default=False, description='Only build TOPK primitive')

    variant('boost', default=False, description='Build with Boost')
    variant('metis', default=False, description='Build with Metis support')

    depends_on('googletest', when='+google_tests')
    depends_on('lcov', when='+code_coverage')
    depends_on('boost', when='+boost')
    depends_on('metis', when='+metis')

    msg = 'all_applications variant is enabled by default. \
Turn it off explicitly in order to build individual apps like: \n\
    spack install gunrock ~all_applicatins +app_bc'

    conflicts('+all_applications', when='+app_bc',      msg=msg)
    conflicts('+all_applications', when='+app_bfs',     msg=msg)
    conflicts('+all_applications', when='+app_cc',      msg=msg)
    conflicts('+all_applications', when='+app_pr',      msg=msg)
    conflicts('+all_applications', when='+app_sssp',    msg=msg)
    conflicts('+all_applications', when='+app_dobfs',   msg=msg)
    conflicts('+all_applications', when='+app_hits',    msg=msg)
    conflicts('+all_applications', when='+app_salsa',   msg=msg)
    conflicts('+all_applications', when='+app_mst',     msg=msg)
    conflicts('+all_applications', when='+app_wtf',     msg=msg)
    conflicts('+all_applications', when='+app_topk',    msg=msg)

    conflicts('cuda_arch=none', when='+cuda',
              msg='Must specify CUDA compute capabilities of your GPU. \
See "spack info gunrock"')


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
                    '-DCUDA_VERBOSE_PTXAS={0}'.format(
                        'ON' if '+cuda_verbose_ptxas' in spec else 'OFF'),
                    '-DGUNROCK_GOOGLE_TESTS={0}'.format(
                        'ON' if '+google_tests' in spec else 'OFF'),
                    '-DGUNROCK_CODE_COVERAGE={0}'.format(
                        'ON' if '+code_coverage' in spec else 'OFF'),
                    '-DGUNROCK_BUILD_APPLICATIONS={0}'.format(
                        'ON' if '+all_applications' in spec else 'OFF'),
                    '-DGUNROCK_APP_BC={0}'.format(
                        'OFF' if '+app_bc' in spec else 'OFF'),
                    '-DGUNROCK_APP_BFS={0}'.format(
                        'OFF' if '+app_bfs' in spec else 'OFF'),
                    '-DGUNROCK_APP_CC={0}'.format(
                        'OFF' if '+app_cc' in spec else 'OFF'),
                    '-DGUNROCK_APP_PR={0}'.format(
                        'OFF' if '+app_pr' in spec else 'OFF'),
                    '-DGUNROCK_APP_SSSP={0}'.format(
                        'OFF' if '+app_sssp' in spec else 'OFF'),
                    '-DGUNROCK_APP_DOBFS={0}'.format(
                        'OFF' if '+app_dobfs' in spec else 'OFF'),
                    '-DGUNROCK_APP_HITS={0}'.format(
                        'OFF' if '+app_hits' in spec else 'OFF'),
                    '-DGUNROCK_APP_SALSA={0}'.format(
                        'OFF' if '+app_salsa' in spec else 'OFF'),
                    '-DGUNROCK_APP_MST={0}'.format(
                        'OFF' if '+app_mst' in spec else 'OFF'),
                    '-DGUNROCK_APP_WTF={0}'.format(
                        'OFF' if '+app_wtf' in spec else 'OFF'),
                    '-DGUNROCK_APP_TOPK={0}'.format(
                        'OFF' if '+app_topk' in spec else 'OFF'),
                    ])

        cuda_arch_list = self.spec.variants['cuda_arch'].value
        if cuda_arch_list[0] != 'none':
            for carch in cuda_arch_list:
                args.append('-DGUNROCK_BUILD_GENCODE_SM' + carch + '=ON')

        return args

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            install_tree('lib', prefix.lib)
            if '+tests' in spec:
                install_tree('bin', prefix.bin)
