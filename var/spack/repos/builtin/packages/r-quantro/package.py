# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RQuantro(RPackage):
    """A data-driven test for the assumptions of quantile normalization using
       raw data such as objects that inherit eSets (e.g. ExpressionSet,
       MethylSet). Group level information about each sample (such as
       Tumor / Normal status) must also be provided because the test assesses
       if there are global differences in the distributions between the
       user-defined groups."""

    homepage = "https://www.bioconductor.org/packages/quantro/"
    git      = "https://git.bioconductor.org/packages/quantro.git"

    version('1.10.0', commit='111337c0aba052aa49c3d2e2d3042794b28858c9')

    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-minfi', type=('build', 'run'))
    depends_on('r-doparallel', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-iterators', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.10.0')
