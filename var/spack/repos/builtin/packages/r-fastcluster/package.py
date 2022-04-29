# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RFastcluster(RPackage):
    """Fast Hierarchical Clustering Routines for R and 'Python'.

    This is a two-in-one package which provides interfaces to both R and
    'Python'. It implements fast hierarchical, agglomerative clustering
    routines. Part of the functionality is designed as drop-in replacement for
    existing routines: linkage() in the 'SciPy' package
    'scipy.cluster.hierarchy', hclust() in R's 'stats' package, and the
    'flashClust' package. It provides the same functionality with the benefit
    of a much faster implementation. Moreover, there are memory-saving routines
    for clustering of vector data, which go beyond what the existing packages
    provide. For information on how to install the 'Python' files, see the file
    INSTALL in the source distribution."""

    cran = "fastcluster"

    version('1.2.3', sha256='1f229129e1cddc78c7bb5ecc90c4d28ed810ee68cf210004c7cdfa12cfaf2a01')
    version('1.1.25', sha256='f3661def975802f3dd3cec5b2a1379f3707eacff945cf448e33aec0da1ed4205')

    depends_on('r@3.0.0:', type=('build', 'run'))
