# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RYaqcaffy(RPackage):
    """Quality control of Affymetrix GeneChip expression data and
       reproducibility analysis of human whole genome chips with the MAQC
       reference datasets."""

    homepage = "http://bioconductor.org/packages/yaqcaffy/"
    git      = "https://git.bioconductor.org/packages/yaqcaffy.git"

    version('1.36.0', commit='4d46fe77b2c8de2230a77b0c07dd5dd726e3abd6')

    depends_on('r-simpleaffy', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.36.0')
