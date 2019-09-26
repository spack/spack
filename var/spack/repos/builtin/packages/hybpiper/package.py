# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob
import os


class Hybpiper(Package):
    """HybPiper was designed for targeted sequence capture, in which DNA
       sequencing libraries are enriched for gene regions of interest,
       especially for phylogenetics. HybPiper is a suite of Python scripts
       that wrap and connect bioinformatics tools in order to extract target
       sequences from high-throughput DNA sequencing reads"""

    homepage = "https://github.com/mossmatters/HybPiper"
    url      = "https://github.com/mossmatters/HybPiper/archive/v1.2.0.tar.gz"
    git      = "https://github.com/mossmatters/HybPiper/HybPiper.git"

    version('1.3.1', sha256='7ca07a9390d1ca52c72721774fa220546f18d3fa3b58500f68f3b2d89dbc0ecf')
    version('1.2.0', '0ad78e9ca5e3f23ae0eb6236b07e1780')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-biopython', type=('build', 'run'))
    depends_on('exonerate')
    depends_on('blast-plus')
    depends_on('spades')
    depends_on('parallel')
    depends_on('bwa')
    depends_on('samtools')

    def setup_envionment(self, spack_env, run_env):
        run_env.set('HYBPIPER_HOME', prefix)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        files = glob.iglob("*.py")
        for file in files:
            if os.path.isfile(file):
                install(file, prefix.bin)
