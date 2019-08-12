# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Rsbench(MakefilePackage):
    """A mini-app to represent the multipole resonance representation lookup
       cross section algorithm."""

    homepage = "https://github.com/ANL-CESAR/RSBench"
    url = "https://github.com/ANL-CESAR/RSBench/archive/v2.tar.gz"

    version('2', '15a3ac5ea72529ac1ed9ed016ee68b4f')
    version('0', '3427634dc5e7cd904d88f9955b371757')

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
