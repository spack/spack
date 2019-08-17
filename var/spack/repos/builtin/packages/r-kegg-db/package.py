# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RKeggDb(RPackage):
    """A set of annotation maps for KEGG assembled using data from KEGG."""

    homepage = "https://www.bioconductor.org/packages/KEGG.db/"
    url = "https://www.bioconductor.org/packages/release/data/annotation/src/contrib/KEGG.db_3.2.3.tar.gz"

    version('3.2.3', '023ac22f57063627c2e62d1ae5e011b0')
    depends_on('r-annotationdbi', type=('build', 'run'))
