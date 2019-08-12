# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAltcdfenvs(RPackage):
    """Convenience data structures and functions to handle cdfenvs."""

    homepage = "https://www.bioconductor.org/packages/altcdfenvs/"
    git      = "https://git.bioconductor.org/packages/altcdfenvs.git"

    version('2.38.0', commit='2e92b9da76dbe50af4bf33c525134e29e9809291')

    depends_on('r@3.4.0:3.4.9', when='@2.38.0')
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-makecdfenv', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-hypergraph', type=('build', 'run'))
