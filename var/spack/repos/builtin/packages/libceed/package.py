# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libceed(Package):
    """The CEED API Library: Code for Efficient Extensible Discretizations."""

    homepage = "https://github.com/CEED/libCEED"
    git      = "https://github.com/CEED/libCEED.git"

    version('develop', branch='master')
    version('0.5', tag='v0.5')
    version('0.4', tag='v0.4')
    version('0.2', tag='v0.2')
    version('0.1', tag='v0.1')

    variant('occa', default=True, description='Enable OCCA backends')
    variant('cuda', default=False, description='Enable CUDA support')
    variant('debug', default=False, description='Enable debug build')
    variant('libxsmm', default=False, description='Enable LIBXSMM backend')

    conflicts('+libxsmm', when='@:0.2')

    depends_on('cuda', when='+cuda')

    depends_on('occa@develop', when='@develop+occa')
    depends_on('occa@1.0.8:', when='@0.4+occa')
    depends_on('occa@1.0.0-alpha.5,develop', when='@:0.2+occa')
    depends_on('occa+cuda', when='+occa+cuda')
    depends_on('occa~cuda', when='+occa~cuda')

    depends_on('libxsmm', when='+libxsmm')

    patch('pkgconfig-version-0.4.diff', when='@0.4')

    # occa: do not occaFree kernels
    # Repeated creation and freeing of kernels appears to expose a caching
    # bug in Occa.
    patch('occaFree-0.2.diff', when='@0.2')

    phases = ['build', 'install']

    @property
    def common_make_opts(self):
        spec = self.spec
        compiler = self.compiler
        # Note: The occa package exports OCCA_DIR in the environment

        # Use verbose building output
        makeopts = ['V=1']

        if '@:0.2' in spec:
            makeopts += ['NDEBUG=%s' % ('' if '+debug' in spec else '1')]

        elif '@0.4:' in spec:
            # Determine options based on the compiler:
            if '+debug' in spec:
                opt = '-g'
            elif compiler.name == 'gcc':
                opt = '-O3 -g -ffp-contract=fast'
                if compiler.target in ['x86_64']:
                    opt += ' -march=native'
                elif compiler.target in ['ppc64le']:
                    opt += ' -mcpu=native -mtune=native'
                if compiler.version >= ver(4.9):
                    opt += ' -fopenmp-simd'
            elif compiler.name == 'clang':
                opt = '-O3 -g -march=native -ffp-contract=fast'
                if compiler.version.string.endswith('-apple'):
                    if compiler.version >= ver(10):
                        opt += ' -fopenmp-simd'
                else:  # not apple clang
                    if compiler.version >= ver(6):
                        opt += ' -fopenmp-simd'
            elif compiler.name in ['xl', 'xl_r']:
                opt = '-O -g -qsimd=auto'
            else:
                opt = '-O -g'
            makeopts += ['OPT=%s' % opt]

            if '+cuda' in spec:
                makeopts += ['CUDA_DIR=%s' % spec['cuda'].prefix]
                nvccflags = ['-ccbin %s -Xcompiler "%s" -Xcompiler %s' %
                             (compiler.cxx, opt, compiler.pic_flag)]
                nvccflags = ' '.join(nvccflags)
                makeopts += ['NVCCFLAGS=%s' % nvccflags]
            else:
                # Disable CUDA auto-detection:
                makeopts += ['CUDA_DIR=/disable-cuda']

            if '+libxsmm' in spec:
                makeopts += ['XSMM_DIR=%s' % spec['libxsmm'].prefix]

        return makeopts

    def build(self, spec, prefix):
        makeopts = self.common_make_opts
        make('info', *makeopts)
        make(*makeopts)

        if self.run_tests:
            make('prove', *makeopts, parallel=False)

    def install(self, spec, prefix):
        installopts = ['prefix=%s' % prefix]
        installopts += self.common_make_opts
        make('install', *installopts, parallel=False)

    @when('@0.1')
    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install('ceed.h', prefix.include)
        mkdirp(prefix.lib)
        install('libceed.%s' % dso_suffix, prefix.lib)
        filter_file(r'^prefix=.*$', 'prefix=%s' % prefix, 'ceed.pc')
        filter_file(r'^includedir=\$\{prefix\}$',
                    'includedir=${prefix}/include', 'ceed.pc')
        filter_file(r'^libdir=\$\{prefix\}$',
                    'libdir=${prefix}/lib', 'ceed.pc')
        filter_file(r'Version:.*$', 'Version: 0.1', 'ceed.pc')
        mkdirp(prefix.lib.pkgconfig)
        install('ceed.pc', prefix.lib.pkgconfig)
