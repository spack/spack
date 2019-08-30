# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSeqinr(RPackage):
    """Exploratory data analysis and data visualization for biological
    sequence (DNA and protein) data. Includes also utilities for sequence
    data management under the ACNUC system."""

    homepage = "http://seqinr.r-forge.r-project.org"
    url      = "https://cloud.r-project.org/src/contrib/seqinr_3.3-6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/seqinr"

    version('3.4-5', 'd550525dcea754bbd5b83cb46b4124cc')
    version('3.3-6', '73023d627e72021b723245665e1ad055')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-ade4', type=('build', 'run'))
    depends_on('r-segmented', type=('build', 'run'))
    depends_on('zlib')
