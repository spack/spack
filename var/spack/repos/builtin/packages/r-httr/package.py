# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RHttr(RPackage):
    """Useful tools for working with HTTP organised by HTTP verbs (GET(),
    POST(), etc). Configuration functions make it easy to control additional
    request components (authenticate(), add_headers() and so on)."""

    homepage = "https://github.com/hadley/httr"
    url      = "https://cran.r-project.org/src/contrib/httr_1.2.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/httr"

    version('1.3.1', '5acfb6b2a6f2f26cd6dfad0458fe3351')
    version('1.2.1', 'c469948dedac9ab3926f23cf484b33d9')
    version('1.1.0', '5ffbbc5c2529e49f00aaa521a2b35600')

    depends_on('r@3.0.0:')

    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-mime', type=('build', 'run'))
    depends_on('r-curl@0.9.1:', type=('build', 'run'))
    depends_on('r-openssl', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
