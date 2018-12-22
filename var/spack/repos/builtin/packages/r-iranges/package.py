# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RIranges(RPackage):
    """Provides efficient low-level and highly
    reusable S4 classes for storing,
    manipulating and aggregating over annotated ranges of
    integers. Implements an
    algebra of range operations, including efficient
    algorithms for finding overlaps
    and nearest neighbors. Defines efficient list-like
    classes for storing, transforming
    and aggregating large grouped data,
    i.e., collections of atomic vectors and DataFrames."""

    homepage = "https://www.bioconductor.org/packages/IRanges/"
    git      = "https://git.bioconductor.org/packages/IRanges.git"

    version('2.14.10', commit='c76118a38e84c7c764141adbd66ee350d0882bc9')
    version('2.12.0', commit='1b1748655a8529ba87ad0f223f035ef0c08e7fcd')
    version('2.10.5', commit='b00d1d5025e3c480d17c13100f0da5a0132b1614')

    depends_on('r-biocgenerics@0.21.1:', type=('build', 'run'), when='@2.10.5')
    depends_on('r-biocgenerics@0.23.3:', type=('build', 'run'), when='@2.12.0')
    depends_on('r-biocgenerics@0.25.3:', type=('build', 'run'), when='@2.14.10')
    depends_on('r-s4vectors@0.13.17:', type=('build', 'run'), when='@2.10.5')
    depends_on('r-s4vectors@0.15.5:', type=('build', 'run'), when='@2.12.0')
    depends_on('r-s4vectors@0.18.2:', type=('build', 'run'), when='@2.14.10')
    depends_on('r@3.4.0:3.4.9', when='@2.10.5', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@2.14.10', type=('build', 'run'))
