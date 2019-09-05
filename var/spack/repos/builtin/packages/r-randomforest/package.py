# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRandomforest(RPackage):
    """Classification and regression based on a forest of trees using random
    inputs."""

    homepage = "https://www.stat.berkeley.edu/~breiman/RandomForests/"
    url      = "https://cloud.r-project.org/src/contrib/randomForest_4.6-12.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/randomForest"

    version('4.6-14', sha256='f4b88920419eb0a89d0bc5744af0416d92d112988702dc726882394128a8754d')
    version('4.6-12', '071c03af974198e861f1475c5bab9e7a')

    depends_on('r@2.5.0:', when='@:4.6-12', type=('build', 'run'))
    depends_on('r@3.2.2:', when='@4.6-14:', type=('build', 'run'))
