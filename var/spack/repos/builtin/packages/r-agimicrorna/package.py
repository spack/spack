# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAgimicrorna(RPackage):
    """Processing and Analysis of Agilent microRNA data."""

    homepage = "https://www.bioconductor.org/packages/AgiMicroRna/"
    git      = "https://git.bioconductor.org/packages/AgiMicroRna.git"

    version('2.26.0', commit='6dd74bae47986f2a23d03e3f1f9f78f701dd8053')

    depends_on('r@3.4.0:3.4.9', when='@2.26.0')
    depends_on('r-affycoretools', type=('build', 'run'))
    depends_on('r-preprocesscore', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
