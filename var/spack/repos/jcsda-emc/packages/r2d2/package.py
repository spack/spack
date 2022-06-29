# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os


class R2d2(PythonPackage):
    """Research Repository for Data and Diagnostics (R2D2) - DH* NEED TO FILL IN THE DETAILS
    """

    homepage = "https://github.com/JCSDA/r2d2"
    git = "https://github.com/JCSDA/r2d2.git"
    url = "https://github.com/JCSDA/r2d2/archive/refs/tags/1.0.0.tar.gz"

    maintainers = ['climbfuji', 'ericlingerfelt']

    version('develop', branch='develop', no_cache=True)
    version('0.0.1', commit='011990d36c9c651593e5e158b5ad7ef07aee16dc', preferred=True)

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-pyyaml@5.3.1:', type=('build', 'run'))
    depends_on('py-boto3', type=('build', 'run'))
