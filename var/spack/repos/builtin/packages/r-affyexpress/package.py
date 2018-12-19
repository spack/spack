# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAffyexpress(RPackage):
    """The purpose of this package is to provide a comprehensive and
    easy-to-use tool for quality assessment and to identify differentially
    expressed genes in the Affymetrix gene expression data."""

    homepage = "https://www.bioconductor.org/packages/AffyExpress/"
    git      = "https://git.bioconductor.org/packages/AffyExpress.git"

    version('1.42.0', commit='f5c5cf6173f4419e25f4aeff5e6b705a40abc371')

    depends_on('r@3.4.0:3.4.9', when='@1.42.0')
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
