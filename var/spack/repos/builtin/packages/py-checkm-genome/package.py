# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCheckmGenome(PythonPackage):
    """Assess the quality of microbial genomes recovered from isolates, single
    cells, and metagenomes"""

    homepage = "https://ecogenomics.github.io/CheckM"
    url      = "https://pypi.io/packages/source/c/checkm-genome/checkm-genome-1.0.11.tar.gz"

    version('1.0.11', '3058546ec324e2420cf72f0d2576114b')

    depends_on('hmmer@3.1b1:')
    depends_on('prodigal@2.6.1:')
    depends_on('py-numpy@1.8.0:',        type=('build', 'run'))
    depends_on('py-scipy@0.9.0:',        type=('build', 'run'))
    depends_on('py-matplotlib@1.3.1:',   type=('build', 'run'))
    depends_on('py-pysam@0.8.3:',        type=('build', 'run'))
    depends_on('py-dendropy@4.0.0:',     type=('build', 'run'))
