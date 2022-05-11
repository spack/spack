# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RGh(RPackage):
    """'GitHub' 'API'.

    Minimal client to access the 'GitHub' 'API'."""

    cran = "gh"

    version('1.3.0', sha256='a44039054e8ca56496f2d9c7a10cdadf4a7383bc91086e768ba7e7f1fbcaed1c')
    version('1.2.0', sha256='2988440ed2ba4b241c8ffbafbfdad29493574980a9aeba210521dadda91f7eff')
    version('1.1.0', sha256='de9faf383c3fe5e87a75391d82cf71b1331b3c80cd00c4203146a303825d89ad')
    version('1.0.1', sha256='f3c02b16637ae390c3599265852d94b3de3ef585818b260d00e7812595b391d2')

    depends_on('r-cli', type=('build', 'run'), when='@1.1.0:')
    depends_on('r-cli@2.0.1:', type=('build', 'run'), when='@1.2.0:')
    depends_on('r-gitcreds', type=('build', 'run'), when='@1.2.0:')
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-httr@1.2:', type=('build', 'run'), when='@1.1.0:')
    depends_on('r-ini', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
