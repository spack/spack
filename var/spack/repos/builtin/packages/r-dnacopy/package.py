# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDnacopy(RPackage):
    """Implements the circular binary segmentation (CBS) algorithm
    to segment DNA copy number data and identify genomic regions
    with abnormal copy number."""

    homepage = "https://www.bioconductor.org/packages/DNAcopy/"
    git      = "https://git.bioconductor.org/packages/DNAcopy.git"

    version('1.50.1', commit='a20153029e28c009df813dbaf13d9f519fafa4e8')
