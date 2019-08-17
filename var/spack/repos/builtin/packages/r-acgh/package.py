# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAcgh(RPackage):
    """Functions for reading aCGH data from image analysis output files
    and clone information files, creation of aCGH S3 objects for storing
    these data. Basic methods for accessing/replacing, subsetting,
    printing and plotting aCGH objects."""

    homepage = "https://www.bioconductor.org/packages/aCGH/"
    git      = "https://git.bioconductor.org/packages/aCGH.git"

    version('1.54.0', commit='be2ed339449f55c8d218e10c435e4ad356683693')

    depends_on('r@3.4.0:3.4.9', when='@1.54.0')
    depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-multtest', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
