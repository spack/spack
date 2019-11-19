# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBiocparallel(RPackage):
    """This package provides modified versions and novel implementation of
       functions for parallel evaluation, tailored to use with Bioconductor
       objects."""

    homepage = "https://bioconductor.org/packages/BiocParallel/"
    url     = "https://bioconductor.org/packages/release/bioc/src/contrib/BiocParallel_1.20.0.tar.gz"

    version('1.20.0', sha256='9aff5449e966c6301288edbcee17e37a0ff8f2eda7d544bb47b627044853f6f1')

    depends_on('r-futile-logger', type=('build', 'run'))
    depends_on('r-snow', type=('build', 'run'))
    depends_on('r-bh', type=('build', 'link', 'run'), when='@1.14.2:')
