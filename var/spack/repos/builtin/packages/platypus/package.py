# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Platypus(Package):
    """A Haplotype-Based Variant Caller For Next Generation Sequence Data"""

    homepage = "http://www.well.ox.ac.uk/platypus"
    url      = "http://www.well.ox.ac.uk/bioinformatics/Software/Platypus-latest.tgz"

    version('0.8.1', 'edf3fb5bf080241ddb75a413c8529d57')

    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('py-cython', type='build')
    depends_on('htslib')

    def install(self, spec, prefix):
        build_platypus = Executable('./buildPlatypus.sh')
        build_platypus()
        install_tree('.', prefix.bin)
