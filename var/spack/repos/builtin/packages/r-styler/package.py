# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RStyler(RPackage):
    """Non-Invasive Pretty Printing of R Code.

    Pretty-prints R code without changing the user's formatting intent."""

    cran = "styler"

    version('1.6.2', sha256='a62fcc76aac851069f33874f9eaabdd580973b619cfc625d6ec910476015f75c')
    version('1.3.2', sha256='3fcf574382c607c2147479bad4f9fa8b823f54fb1462d19ec4a330e135a44ff1')

    depends_on('r-backports@1.1.0:', type=('build', 'run'))
    depends_on('r-cli@1.1.0:', type=('build', 'run'))
    depends_on('r-glue', type=('build', 'run'), when='@1.6.2:')
    depends_on('r-magrittr@1.0.1:', type=('build', 'run'))
    depends_on('r-magrittr@2.0.0:', type=('build', 'run'), when='@1.6.2:')
    depends_on('r-purrr@0.2.3:', type=('build', 'run'))
    depends_on('r-r-cache@0.14.0:', type=('build', 'run'))
    depends_on('r-r-cache@0.15.0:', type=('build', 'run'), when='@1.6.2:')
    depends_on('r-rematch2@2.0.1:', type=('build', 'run'))
    depends_on('r-rlang@0.1.1:', type=('build', 'run'))
    depends_on('r-rprojroot@1.1:', type=('build', 'run'))
    depends_on('r-tibble@1.4.2:', type=('build', 'run'))
    depends_on('r-withr@1.0.0:', type=('build', 'run'))
    depends_on('r-xfun@0.1:', type=('build', 'run'))
