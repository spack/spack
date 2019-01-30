# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAims(RPackage):
    """This package contains the AIMS implementation. It contains
    necessary functions to assign the five intrinsic molecular
    subtypes (Luminal A, Luminal B, Her2-enriched, Basal-like,
    Normal-like). Assignments could be done on individual samples
    as well as on dataset of gene expression data."""

    homepage = "http://bioconductor.org/packages/AIMS/"
    git      = "https://git.bioconductor.org/packages/AIMS.git"

    version('1.8.0', commit='86b866c20e191047492c51b43e3f73082c3f8357')

    depends_on('r@3.4.0:3.4.9', when='@1.8.0')
    depends_on('r-e1071', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
