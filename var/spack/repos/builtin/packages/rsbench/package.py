# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Rsbench(MakefilePackage):
    """A mini-app to represent the multipole resonance representation lookup
       cross section algorithm."""

    homepage = "https://github.com/ANL-CESAR/RSBench"
    url = "https://github.com/ANL-CESAR/RSBench/archive/v2.tar.gz"

    version('12', sha256='2e437dbdaf7bf12bb9ade429d46a9e74fd519fc4686777a452770790d0546499')
    version('11', sha256='8e3b806626fe803ef6284c1e20a05063fc89be153c81e4bd629b6db82eaed3da')
    version('10', sha256='180ceec6ac7a0b8107b897d428d640abc22a18c6c65101a348e409e5db3505cc')
    version('2', sha256='1e97a38a863836e98cedc5cc669f8fdcaed905fafdc921d2bce32319b3e157ff')
    version('0', sha256='95c06cf4cb6f396f9964d5e4b58a477bf9d7131cd39804480f1cb74e9310b271')

    tags = ['proxy-app']

    build_directory = 'src'

    @property
    def build_targets(self):
        targets = []

        cflags = '-std=gnu99'
        ldflags = '-lm'

        if self.compiler.name == 'gcc':
            cflags += ' -ffast-math '
        elif self.compiler.name == 'intel':
            cflags += ' -xhost -ansi-alias -no-prec-div '
        elif self.compiler.name == 'pgi':
            cflags += ' -fastsse '

        cflags += self.compiler.openmp_flag

        targets.append('CFLAGS={0}'.format(cflags))
        targets.append('LDFLAGS={0}'.format(ldflags))

        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('src/rsbench', prefix.bin)
