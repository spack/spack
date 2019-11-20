# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RXde(RPackage):
    """Multi-level model for cross-study detection of differential gene
       expression."""

    homepage = "https://www.bioconductor.org/packages/XDE/"
    git      = "https://git.bioconductor.org/packages/XDE.git"

    version('2.22.0', commit='25bcec965ae42a410dd285a9db9be46d112d8e81')

    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-gtools', type=('build', 'run'))
    depends_on('r-mergemaid', type=('build', 'run'))
    depends_on('r-mvtnorm', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.22.0')
