# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fftx(CMakePackage, CudaPackage, ROCmPackage):
    """FFTX is the exascale follow-on to the FFTW open source discrete FFT
    package for executing the Fast Fourier Transform as well as higher-level
    operations composed of linear operations combined with DFT transforms."""

    homepage = "https://spiral.net"
    url      = "https://github.com/spiral-software/fftx/archive/1.0.1-release.tar.gz"
    git      = "https://github.com/spiral-software/fftx.git"

    maintainers = ['spiralgen']

    version('develop', branch='develop')
    version('main',  branch='main')
    version('1.0.2-release', sha256='008007109866438e861dd7df27263d098b5ee8b143bfc9b43ea40eac7d0915a0')
    version('1.0.1-release', sha256='af9c3a8b964dce5cf9a524ee2d08d283be7d12cb939b48c75c3d3c14812fe218')
    version('1.0.0-release', sha256='e3b39b187a3b20badfe766e9d968049280906b2fbbef371321b2ece2460eedb4')
    version('0.9.0', sha256='d4930e9b959fd56bb63543b359ca09a7ae2c56db3ffc28d7d3628d92fc79ce12')

    variant('build_type', default='Release',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'),
            description='The build type to build')

    depends_on('spiral-software')
    depends_on('spiral-package-fftx')
    depends_on('spiral-package-simt')
    #  depends_on('spiral-package-mpi')

    conflicts('+rocm', when='+cuda', msg='FFTX only supports one GPU backend at a time')

    @run_before('cmake')
    def create_lib_source_code(self):
        #  What config should be built -- driven by spec
        spec = self.spec
        backend = 'CPU'
        if '+cuda' in spec:
            backend = 'CUDA'
        if '+rocm' in spec:
            backend = 'HIP'
        self.build_config = '-D_codegen=%s' % backend

        #  From directory examples/library run the build-lib-code.sh script
        with working_dir(join_path(self.stage.source_path, 'examples', 'library')):
            bash = which('bash')
            bash('./build-lib-code.sh', backend)

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DSPIRAL_HOME:STRING={0}'.format(spec['spiral-software'].prefix)
        ]
        args.append('-DCMAKE_INSTALL_PREFIX:PATH={0}'.format(self.stage.source_path))
        args.append(self.build_config)
        print('Args = ' + str(args))
        return args

    @property
    def build_targets(self):
        return ['install']

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.CMakeIncludes)
        mkdirp(prefix.examples)
        mkdirp(prefix.include)
        mkdirp(prefix.lib)

        with working_dir(self.stage.source_path):
            files = ('License.txt', 'README.md', 'ReleaseNotes.md')
            for fil in files:
                install(fil, prefix)

        with working_dir(self.stage.source_path):
            install_tree('bin', prefix.bin)
            install_tree('CMakeIncludes', prefix.CMakeIncludes)
            install_tree('examples', prefix.examples)
            install_tree('include', prefix.include)
            install_tree('lib', prefix.lib)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('FFTX_HOME', self.prefix)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set('FFTX_HOME', self.prefix)

    def setup_run_environment(self, env):
        env.set('FFTX_HOME', self.prefix)
