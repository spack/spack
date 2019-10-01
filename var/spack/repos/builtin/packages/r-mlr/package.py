# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMlr(RPackage):
    """Interface to a large number of classification and regression techniques,
       including machine-readable parameter descriptions. There is also an
       experimental extension for survival analysis, clustering and general,
       example-specific cost-sensitive learning. Generic resampling,
       including cross-validation, bootstrapping and subsampling.
       Hyperparameter tuning with modern optimization techniques,
       for single- and multi-objective problems. Filter and wrapper methods for
       feature selection. Extension of basic learners with additional
       operations common in machine learning, also allowing for easy nested
       resampling. Most operations can be parallelized."""

    homepage = "https://github.com/mlr-org/mlr/"
    url      = "https://cloud.r-project.org/src/contrib/mlr_2.12.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/mlr"

    version('2.15.0', sha256='a3c2c2bd65a87d90b5e5e877b1ef8e7712e76b4eb1660d3f69672a1860ca5324')
    version('2.14.0', sha256='1f72184400678386c7c44297c4c92a448b50148de700df5ba0438d4e486e944a')
    version('2.13', sha256='e8729be7acddc1ea124c44f9493a8b903c5f54b97e09c714366553aed733011d')
    version('2.12.1', 'abddfc9dfe95f290a233ecd97969a4ec')
    version('2.12', '94ee7495aeafb432c8af5a8bdd26c25f')

    depends_on('r@3.0.2:', type=('build', 'run'))
    depends_on('r-paramhelpers@1.10:', type=('build', 'run'))
    depends_on('r-bbmisc@1.11:', type=('build', 'run'))
    depends_on('r-backports@1.1.0:', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-stringi', type=('build', 'run'))
    depends_on('r-checkmate@1.8.2:', type=('build', 'run'))
    depends_on('r-data-table', type=('build', 'run'))
    depends_on('r-parallelmap@1.3:', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-xml', type=('build', 'run'))
