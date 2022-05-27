# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RIlluminaio(RPackage):
    """Parsing Illumina Microarray Output Files.

       Tools for parsing Illumina's microarray output files, including IDAT."""

    bioc = "illuminaio"

    version('0.36.0', commit='c5b6e9164b73c650c0a9f055f4fd0580ac64fae7')
    version('0.32.0', commit='e1322c781dd475a5e8ff6c0422bebb3deb47fa80')
    version('0.26.0', commit='40c2f94df2ea64d745d25aadd2bfb33ac3e02f81')
    version('0.24.0', commit='47953c77713c2da00a610f39308f86c5b44f6c59')
    version('0.22.0', commit='dbd842340999569975ea593f47d70a729b3f68f2')
    version('0.20.0', commit='d226628133b2396be9e7a6bf043f0309bd70c4ec')
    version('0.18.0', commit='e6b8ab1f8eacb760aebdb4828e9cfbf07da06eda')

    depends_on('r-base64', type=('build', 'run'))
