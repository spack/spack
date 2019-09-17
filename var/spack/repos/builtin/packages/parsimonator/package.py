# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.spec import ConflictsInSpecError


class Parsimonator(MakefilePackage):
    """Parsimonator is a no-frills light-weight implementation for building
       starting trees under parsimony for RAxML"""

    homepage = "http://www.exelixis-lab.org/"
    git      = "https://github.com/stamatak/Parsimonator-1.0.2.git"

    version('1.0.2', commit='78368c6ab1e9adc7e9c6ec9256dd7ff2a5bb1b0a')

    variant('sse', default=False, description='Enable SSE in order to substantially speed up execution')
    variant('avx', default=False, description='Enable AVX in order to substantially speed up execution')

    conflicts('+avx', when='+sse')

    patch('nox86.patch')

    def flag_handler(self, name, flags):
        arch = ''
        spec = self.spec
        if spec.satisfies("platform=cray"):
            # FIXME; It is assumed that cray is x86_64.
            # If you support arm on cray, you need to fix it.
            arch = 'x86_64'
        if arch != 'x86_64' and spec.target.family != 'x86_64':
            if spec.satisfies("+sse"):
                raise ConflictsInSpecError(
                    spec,
                    [(
                        spec,
                        spec.architecture.target,
                        spec.variants['sse'],
                        '+sse is valid only on x86_64'
                    )]
                )
            if spec.satisfies("+avx"):
                raise ConflictsInSpecError(
                    spec,
                    [(
                        spec,
                        spec.architecture.target,
                        spec.variants['avx'],
                        '+avx is valid only on x86_64'
                    )]
                )
        return (flags, None, None)

    @property
    def makefile_file(self):
        if self.spec.target.family != 'x86_64':
            return 'Makefile.nosse'
        elif '+sse' in self.spec:
            return 'Makefile.SSE3.gcc'
        elif '+avx' in self.spec:
            return 'Makefile.AVX.gcc'
        else:
            return 'Makefile.gcc'

    def edit(self, spec, prefix):
        makefile = FileFilter(self.makefile_file)
        makefile.filter('CC = gcc', 'CC = %s' % spack_cc)

    def build(self, spec, prefix):
        make('-f', self.makefile_file)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        if self.spec.target.family != 'x86_64':
            install('parsimonator', prefix.bin)
        elif '+sse' in spec:
            install('parsimonator-SSE3', prefix.bin)
        elif '+avx' in spec:
            install('parsimonator-AVX', prefix.bin)
        else:
            install('parsimonator', prefix.bin)
