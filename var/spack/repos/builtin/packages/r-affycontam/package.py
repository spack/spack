# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAffycontam(RPackage):
    """structured corruption of cel file data to demonstrate QA
    effectiveness."""

    homepage = "https://www.bioconductor.org/packages/affyContam/"
    git      = "https://git.bioconductor.org/packages/affyContam.git"

    version('1.34.0', commit='03529f26d059c19e069cdda358dbf7789b6d4c40')

    depends_on('r@3.4.0:3.4.9', when=('@1.34.0'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-affydata', type=('build', 'run'))
