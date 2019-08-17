# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAffyqcreport(RPackage):
    """This package creates a QC report for an AffyBatch object.
    The report is intended to allow the user to quickly assess the
    quality of a set of arrays in an AffyBatch object."""

    homepage = "https://www.bioconductor.org/packages/affyQCReport/"
    git      = "https://git.bioconductor.org/packages/affyQCReport.git"

    version('1.54.0', commit='5572e9981dc874b78b4adebf58080cac3fbb69e1')

    depends_on('r@3.4.0:3.4.9', when='@1.54.0')
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-affyplm', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-simpleaffy', type=('build', 'run'))
    depends_on('r-xtable', type=('build', 'run'))
