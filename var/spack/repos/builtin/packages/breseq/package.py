# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Breseq(AutotoolsPackage):
    """breseq is a computational pipeline for finding mutations relative to
    a reference sequence in short-read DNA re-sequencing data for haploid
    microbial-sized genomes."""

    homepage = "http://barricklab.org/breseq"
    url      = "https://github.com/barricklab/breseq/archive/v0.31.1.tar.gz"

    version('0.33.2', sha256='c698d2d25cc7ed251ff916343a8c04f79b5540281288cb7c955f458255ac21de')
    version('0.33.1', sha256='e24a50e254ad026c519747313b9e42bbeb32bd766a6a06ed369bd5b9dc50e84d')
    version('0.31.1', 'a4e602d5481f8692833ba3d5a3cd0394')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    depends_on('zlib', type='build')

    depends_on('bedtools2', type='run')
    depends_on('r', type='run')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('LDFLAGS',
                      "-L{0}".format(self.spec['zlib'].prefix.lib))
        spack_env.set('CFLAGS',
                      "-I{0}".format(self.spec['zlib'].prefix.include))
