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
    version('0.2', tag='v0.2')
    version('0.1', tag='v0.1')

    variant('occa', default=True, description='Enable OCCA backends')
    variant('cuda', default=False, description='Enable CUDA support')
    variant('debug', default=False, description='Enable debug build')

    depends_on('occa@v1.0.0-alpha.5,develop', when='+occa')
    depends_on('occa@develop', when='@develop+occa')
    depends_on('occa+cuda', when='+occa+cuda')
    depends_on('occa~cuda', when='+occa~cuda')

    # occa: do not occaFree kernels
    # Repeated creation and freeing of kernels appears to expose a caching
    # bug in Occa.
    patch('occaFree-0.2.diff', when='@0.2')

    phases = ['build', 'install']

    def build(self, spec, prefix):
        # Note: The occa package exports OCCA_DIR in the environment

        makeopts = ['V=1']
        makeopts += ['NDEBUG=%s' % ('' if '+debug' in spec else '1')]
        make(*makeopts)

        if self.run_tests:
            make('prove', *makeopts, parallel=False)

    def install(self, spec, prefix):
        make('install', 'prefix=%s' % prefix, parallel=False)

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
