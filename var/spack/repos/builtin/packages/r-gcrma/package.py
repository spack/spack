# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGcrma(RPackage):
    """Background adjustment using sequence information"""

    homepage = "https://bioconductor.org/packages/gcrma/"
    git      = "https://git.bioconductor.org/packages/gcrma.git"

    version('2.48.0', commit='3ea0eb0b5c15ffb24df76620667ae7996ed715b4')

    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-affyio', type=('build', 'run'))
    depends_on('r-xvector', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-biocinstaller', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.48.0')
