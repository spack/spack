# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RStyler(RPackage):
    """styler: Non-Invasive Pretty Printing of R Code"""

    homepage = "https://cloud.r-project.org/package=styler"
    url      = "https://cloud.r-project.org/src/contrib/styler_1.3.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/styler"

    version('1.3.2', sha256='3fcf574382c607c2147479bad4f9fa8b823f54fb1462d19ec4a330e135a44ff1')

    depends_on('r-backports@1.1.0:', type=('build', 'run'))
    depends_on('r-cli@1.1.0:', type=('build', 'run'))
    depends_on('r-magrittr@1.0.1:', type=('build', 'run'))
    depends_on('r-purrr@0.2.3:', type=('build', 'run'))
    depends_on('r-r-cache@0.14.0:', type=('build', 'run'))
    depends_on('r-rematch2@2.0.1:', type=('build', 'run'))
    depends_on('r-rlang@0.1.1:', type=('build', 'run'))
    depends_on('r-rprojroot@1.1:', type=('build', 'run'))
    depends_on('r-tibble@1.4.2:', type=('build', 'run'))
    depends_on('r-withr@1.0.0:', type=('build', 'run'))
    depends_on('r-xfun@0.1:', type=('build', 'run'))
