# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBiostrings(RPackage):
    """Memory efficient string containers, string matching algorithms, and
       other utilities, for fast manipulation of large biological sequences
       or sets of sequences."""

    homepage = "https://bioconductor.org/packages/Biostrings/"
    git      = "https://git.bioconductor.org/packages/Biostrings.git"

    version('2.48.0', commit='aa3599a7d259d658014d087b86d71ab1deb5f12b')
    version('2.44.2', commit='e4a2b320fb21c5cab3ece7b3c6fecaedfb1e5200')

    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biocgenerics@0.15.6:', when='@2.48.0', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-s4vectors@0.17.25:', when='@2.48.0', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-iranges@2.13.24:', when='@2.48.0', type=('build', 'run'))
    depends_on('r-xvector', type=('build', 'run'))
    depends_on('r-xvector@0.19.8:', when='@2.48.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.44.2', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@2.48.0', type=('build', 'run'))
