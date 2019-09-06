# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAdabag(RPackage):
    """Applies Multiclass AdaBoost.M1, SAMME and Bagging."""

    homepage = "https://cloud.r-project.org/package=adabag"
    url      = "https://cloud.r-project.org/src/contrib/adabag_4.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/adabag"

    version('4.2', sha256='47019eb8cefc8372996fbb2642f64d4a91d7cedc192690a8d8be6e7e03cd3c81')
    version('4.1', '2e019f053d49f62ebb3b1697bbb50afa')

    depends_on('r-rpart', type=('build', 'run'))
    depends_on('r-mlbench', when='@:4.1', type=('build', 'run'))
    depends_on('r-caret', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-doparallel', type=('build', 'run'))
