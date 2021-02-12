# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bismark(Package):
    """A tool to map bisulfite converted sequence reads and determine cytosine
    methylation states"""

    homepage = "https://www.bioinformatics.babraham.ac.uk/projects/bismark"
    url      = "https://github.com/FelixKrueger/Bismark/archive/0.19.0.tar.gz"

    version('0.23.0', sha256='ea1625808487c1442dbf825d9cbe5c0cbc37ea5bd1460f59e1e0ccc80cc01c9e')
    version('0.22.3', sha256='704523b5cd23a2976ef72484ce3df66208d09220eb71bf9e074446fc881b2e11')
    version('0.22.2', sha256='273b3ba415f70faec70b052cc0b1e29a693e5836811d5fb4ef28370cd8500d29')
    version('0.22.1', sha256='7960302853a1941065a466c1b3a8be6e5b8f7f6dfcf6e747ed711c1056e67ef0')
    version('0.22.0', sha256='6b5c6ec2c0d4a5d3ebe18bae44ea1b6a7f79bfaeb3814578fd41960f43bd55fd')
    version('0.21.0', sha256='0ae3d3db3968a7c03aeadf85e814664278ed59aef0ab891eacab76d44f7acb98')
    version('0.20.1', sha256='596f4cd70d839d6e2e97a858761e1c146972e49634f1941e5672f4ec889b8006')
    version('0.20.0', sha256='825d79e098a5c826edcffcf5b4e7b330b2a368d118857fdbcaa5cb91c2a9b22b')
    version('0.19.1', sha256='9f69bc0090022a6f24d412d580daa5ae5003914d1875c83f3b271397bb37d83e')
    version('0.19.0', sha256='91707737f96a0574956a282b635abad7560e7d90bee188a67a7807b2470deae2')
    version('0.18.2', sha256='83391c5b5af33047178e7774ac25f5a69ce9315c13ae02f016baf7c50b73e702')

    depends_on('bowtie2', type='run')
    depends_on('perl', type='run')
    depends_on('samtools', type='run')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('bam2nuc', prefix.bin)
        install('bismark', prefix.bin)
        install('bismark_genome_preparation', prefix.bin)
        install('bismark_methylation_extractor', prefix.bin)
        install('bismark2bedGraph', prefix.bin)
        install('bismark2report', prefix.bin)
        install('bismark2summary', prefix.bin)
        install('coverage2cytosine', prefix.bin)
        install('deduplicate_bismark', prefix.bin)
        install('filter_non_conversion', prefix.bin)
        install('NOMe_filtering', prefix.bin)
