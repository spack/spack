# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBigalgebra(RPackage):
    """This package provides arithmetic functions for R matrix
       and big.matrix objects."""

    homepage = "https://r-forge.r-project.org/R/?group_id=556"
    url      = "http://download.r-forge.r-project.org/src/contrib/bigalgebra_0.8.4.tar.gz"

    version('0.8.4', sha256='90a064f5d051d3a4b18e453c7fa8bb34d75e952a44f11c6e929413e44a3d6e39')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r-bigmemory')
    depends_on('r-r-methodss3')
    depends_on('r-bh')
