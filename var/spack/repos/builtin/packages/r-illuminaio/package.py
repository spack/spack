# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RIlluminaio(RPackage):
    """Tools for parsing Illumina's microarray output files, including
       IDAT."""

    homepage = "http://bioconductor.org/packages/illuminaio/"
    git      = "https://git.bioconductor.org/packages/illuminaio.git"

    version('0.18.0', commit='e6b8ab1f8eacb760aebdb4828e9cfbf07da06eda')

    depends_on('r-base64', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@0.18.0')
