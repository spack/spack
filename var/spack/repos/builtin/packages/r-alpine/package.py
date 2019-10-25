# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAlpine(RPackage):
    """alpine.

       Fragment sequence bias modeling and correction for RNA-seq transcript
       abundance estimation."""

    homepage = "https://bioconductor.org/packages/alpine"
    git      = "https://git.bioconductor.org/packages/alpine.git"

    version('1.10.0', commit='bf22597eb2c6c6aaa26900ed4ece96ce7256e77c')
    version('1.8.0', commit='ddaa0b4517f0909460aa1bd33c8e43dc6c8d23d4')
    version('1.6.0', commit='ea55fcb3cedb5caa20d8264bb29a4975041f5274')
    version('1.4.0', commit='c85beb208fd6bfc0a61a483a98498b589640f946')
    version('1.2.0', commit='896872e6071769e1ac2cf786974edb8b875c45eb')

    depends_on('r-biostrings', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-genomeinfodb', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-genomicalignments', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-genomicfeatures', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-genomicranges', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-graph', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-iranges', when='@1.2.0:', type=('build', 'run'))
    depends_on('r@3.3:', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-rbgl', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-rsamtools', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-s4vectors', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-speedglm', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-stringr', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-summarizedexperiment', when='@1.2.0:', type=('build', 'run'))
