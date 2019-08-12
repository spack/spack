# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAffy(RPackage):
    """The package contains functions for exploratory oligonucleotide array
       analysis. The dependence on tkWidgets only concerns few convenience
       functions. 'affy' is fully functional without it."""

    homepage = "https://bioconductor.org/packages/affy/"
    git      = "https://git.bioconductor.org/packages/affy.git"

    version('1.54.0', commit='a815f02906fcf491b28ed0a356d6fce95a6bd20e')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-affyio', type=('build', 'run'))
    depends_on('r-biocinstaller', type=('build', 'run'))
    depends_on('r-preprocesscore', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.54.0')
