# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCompositions(RPackage):
    """Compositional Data Analysis"""

    homepage = "https://cloud.r-project.org/package=compositions"
    url      = "https://cloud.r-project.org/src/contrib/compositions_1.40-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/compositions"

    version('1.40-2', 'ad87efe2fb303d95472e73c8ca8d9a01')

    depends_on('r@2.2.0:', type=('build', 'run'))
    depends_on('r-tensora', type=('build', 'run'))
    depends_on('r-robustbase', type=('build', 'run'))
    depends_on('r-energy', type=('build', 'run'))
    depends_on('r-bayesm', type=('build', 'run'))
