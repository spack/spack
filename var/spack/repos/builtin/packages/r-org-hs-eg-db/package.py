# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ROrgHsEgDb(RPackage):
    """Genome wide annotation for Human, primarily based on mapping
    using Entrez Gene identifiers."""

    homepage = "https://bioconductor.org/packages/org.Hs.eg.db/"
    url      = "https://www.bioconductor.org/packages/3.5/data/annotation/src/contrib/org.Hs.eg.db_3.4.1.tar.gz"

    version('3.4.1', '0a987ef7d6167df70e91e6f48145e41c')

    depends_on('r@3.4.0:3.4.9', when='@3.4.1')
    depends_on('r-annotationdbi', type=('build', 'run'))
