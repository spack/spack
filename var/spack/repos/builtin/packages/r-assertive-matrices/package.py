# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAssertiveMatrices(RPackage):
    """assertive.matrices: Assertions to Check Properties of Matrices"""

    homepage = "https://cloud.r-project.org/package=assertive.matrices"
    url      = "https://cloud.r-project.org/src/contrib/assertive.matrices_0.0-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/assertive.matrices"

    version('0.0-2', sha256='3462a7a7e11d7cc24180330d48cc3067cf92eab1699b3e4813deec66d99f5e9b')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-assertive-base@0.0-2:', type=('build', 'run'))
