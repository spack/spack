# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAffycomp(RPackage):
    """The package contains functions that can be used to compare
    expression measures for Affymetrix Oligonucleotide Arrays."""

    homepage = "https://www.bioconductor.org/packages/affycomp/"
    git      = "https://git.bioconductor.org/packages/affycomp.git"

    version('1.52.0', commit='1b97a1cb21ec93bf1e5c88d5d55b988059612790')

    depends_on('r@3.4.0:3.4.9', when='@1.52.0')
    depends_on('r-biobase', type=('build', 'run'))
