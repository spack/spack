# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RQtl(RPackage):
    """Tools for Analyzing QTL Experiments.

    Analysis of experimental crosses to identify genes (called quantitative
    trait loci, QTLs) contributing to variation in quantitative traits. Broman
    et al. (2003) <doi:10.1093/bioinformatics/btg112>."""

    cran = "qtl"

    version('1.50', sha256='2d38656f04dc4187aefe56c29a8f915b8c7e222d76b84afe7045d272294f9ed5')
    version('1.47-9', sha256='6ba4e7b40d946b3ab68d54624599284b1d352c86fb50d31b134826be758ece41')
    version('1.44-9', sha256='315063f0c3fbb95cd2169eb4109ade0339e8f3c28670b38c3167214b9bdf950e')

    depends_on('r@2.14.0:', type=('build', 'run'))
