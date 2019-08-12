# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMiniui(RPackage):
    """Provides UI widget and layout functions for writing Shiny apps that
       work well on small screens."""

    homepage = "https://cran.r-project.org/package=miniUI"
    url      = "https://cran.r-project.org/src/contrib/miniUI_0.1.1.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/miniUI/"

    version('0.1.1.1', sha256='452b41133289f630d8026507263744e385908ca025e9a7976925c1539816b0c0')

    depends_on('r-shiny@0.13:', type=('build', 'run'))
    depends_on('r-htmltools', type=('build', 'run'))
