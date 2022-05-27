# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRandomforest(RPackage):
    """Breiman and Cutler's Random Forests for Classification and Regression.

    Classification and regression based on a forest of trees using random
    inputs."""

    cran = "randomForest"

    version('4.6-14', sha256='f4b88920419eb0a89d0bc5744af0416d92d112988702dc726882394128a8754d')
    version('4.6-12', sha256='6e512f8f88a51c01a918360acba61f1f39432f6e690bc231b7864218558b83c4')

    depends_on('r@2.5.0:', type=('build', 'run'))
    depends_on('r@3.2.2:', type=('build', 'run'), when='@4.6-14:')
