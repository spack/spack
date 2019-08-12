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

    version('3.4.1', '65ed35887ecc44f5ac9f9c8563e03f44')

    depends_on('r@3.4.0:3.4.9', when='@3.4.1')
    depends_on('r-annotationdbi', type=('build', 'run'))
