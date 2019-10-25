# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPfamDb(RPackage):
    """A set of protein ID mappings for PFAM assembled using data from
    public repositories."""

    homepage = "https://www.bioconductor.org/packages/PFAM.db/"
    url      = "https://www.bioconductor.org/packages/3.5/data/annotation/src/contrib/PFAM.db_3.4.1.tar.gz"

    version('3.8.2', sha256='3a951930f6caddfef4b61cb633b4c60c3c40ec268479c2bc1f3e5af67f56c166',
            url='https://www.bioconductor.org/packages/3.9/data/annotation/src/contrib/PFAM.db_3.8.2.tar.gz')
    version('3.4.1', sha256='fc45a0d53139daf85873f67bd3f1b68f2d883617f4447caddbd2d7dcc58a393f')

    depends_on('r@3.4.0:3.4.9', when='@3.4.1')
    depends_on('r@3.6.0:3.6.0', when='@3.8.2')

    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-annotationdbi@1.43.1:', when='@3.8.2:', type=('build', 'run'))
