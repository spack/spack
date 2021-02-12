# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAtropos(PythonPackage):
    """Atropos is tool for specific, sensitive, and speedy trimming of NGS
    reads. It is a fork of the venerable Cutadapt read trimmer."""

    homepage = "https://atropos.readthedocs.io"
    pypi = "atropos/atropos-1.1.22.tar.gz"
    git      = "https://github.com/jdidion/atropos.git"

    version('1.1.29', sha256='904a9e5dedf13bc0d49b06577935bd66ec0d65375f82587ac31cb9eb915f3c50')
    version('1.1.28', sha256='0effe978e4f4e75fdccb68ab3904c99eca7c7b80e98c75e77fc8a48033bca4ae')
    version('1.1.27', sha256='7aabff3e47896fbb287479cc3d27b8902b1b684828140e491d0b357f7bf0c61e')
    version('1.1.26', sha256='d17d566739789a75cf0086403ef587d0dbd2356382d9e73323ad6392d51faed8')
    version('1.1.25', sha256='d09e639baed19c1063596d62dcce5d55ab4c1cebbdca02f0aa049f6a53877cf2')
    version('1.1.24', sha256='fb745ef629a6662fca55129a4414b9811320749a86d65d454a5860fc44905dfd')
    version('1.1.23', sha256='e1a9d030fcaff21a10ca2d5a569451e52f2d6f8f6b2a34ab3574453bda46da9f')
    version('1.1.22', sha256='05e40cb9337421479c692e1154b962fbf811d7939b72c197a024929b7ae88b78')

    depends_on('python@3.3:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-cython@0.25.2:', type='build')
    depends_on('py-tqdm', type=('build', 'run'), when='+tqdm')
    depends_on('py-pysam', type=('build', 'run'), when='+pysam')

    variant('tqdm', default=False, description='Enable progress bar')
    variant('pysam', default=False, description='Enable bam file parsing')
