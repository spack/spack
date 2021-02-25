# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAssertiveModels(RPackage):
    """assertive.models: Assertions to Check Properties of Models"""

    homepage = "https://cloud.r-project.org/package=assertive.models"
    url      = "https://cloud.r-project.org/src/contrib/assertive.models_0.0-2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/assertive.models"

    version('0.0-2', sha256='b9a6d8786f352d53371dbe8c5f2f2a62a7866e30313f268e69626d5c3691c42e')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-assertive-base@0.0-2:', type=('build', 'run'))
