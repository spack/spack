# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSeqlogo(RPackage):
    """seqLogo takes the position weight matrix of a DNA sequence motif and
       plots the corresponding sequence logo as introduced by Schneider and
       Stephens (1990)."""

    homepage = "https://bioconductor.org/packages/seqLogo/"
    git      = "https://git.bioconductor.org/packages/seqLogo.git"

    version('1.44.0', commit='4cac14ff29f413d6de1a9944eb5d21bfe5045fac')

    depends_on('r@3.4.3:3.4.9', when='@1.44.0')
