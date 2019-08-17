# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Transabyss(Package):
    """De novo assembly of RNAseq data using ABySS"""

    homepage = "http://www.bcgsc.ca/platform/bioinfo/software/trans-abyss"
    url      = "http://www.bcgsc.ca/platform/bioinfo/software/trans-abyss/releases/1.5.5/transabyss-1.5.5.zip"

    version('1.5.5', '9ebe0394243006f167135cac4df9bee6')

    depends_on('abyss@1.5.2')
    depends_on('python@2.7.6:', type=('build', 'run'))
    depends_on('py-igraph@0.7.0:', type=('build', 'run'))
    depends_on('blat')

    def install(self, spec, prefix):
        install('transabyss', prefix)
        install('transabyss-merge', prefix)
        install_tree('bin', prefix.bin)
        install_tree('utilities', prefix.utilities)
