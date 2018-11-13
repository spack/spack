# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAffycompatible(RPackage):
    """This package provides an interface to Affymetrix chip annotation
    and sample attribute files. The package allows an easy way for users
    to download and manage local data bases of Affynmetrix NetAffx
    annotation files. The package also provides access to GeneChip
    Operating System (GCOS) and GeneChip Command Console
    (AGCC)-compatible sample annotation files."""

    homepage = "https://www.bioconductor.org/packages/AffyCompatible/"
    git      = "https://git.bioconductor.org/packages/AffyCompatible.git"

    version('1.36.0', commit='dbbfd43a54ae1de6173336683a9461084ebf38c3')

    depends_on('r@3.4.0:3.4.9', when=('@1.36.0'))
    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-rcurl', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
