# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBiocparallel(RPackage):
    """This package provides modified versions and novel implementation of
       functions for parallel evaluation, tailored to use with Bioconductor
       objects."""

    homepage = "https://bioconductor.org/packages/BiocParallel/"
    git      = "https://git.bioconductor.org/packages/BiocParallel.git"

    version('1.14.2', commit='1d5a44960b19e9dbbca04c7290c8c58b0a7fc299')
    version('1.10.1', commit='a76c58cf99fd585ba5ea33065649e68f1afe0a7d')

    depends_on('r-futile-logger', type=('build', 'run'))
    depends_on('r-snow', type=('build', 'run'))
    depends_on('r-bh', type=('build', 'link', 'run'), when='@1.14.2:')
    depends_on('r@3.4.0:3.4.9', when='@1.10.1', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@1.14.2', type=('build', 'run'))
