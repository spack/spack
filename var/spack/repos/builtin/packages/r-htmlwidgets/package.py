# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RHtmlwidgets(RPackage):
    """A framework for creating HTML widgets that render in various contexts
    including the R console, 'R Markdown' documents, and 'Shiny' web
    applications."""

    homepage = "https://cloud.r-project.org/package=htmlwidgets"
    url      = "https://cloud.r-project.org/src/contrib/htmlwidgets_0.9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/htmlwidgets"

    version('1.3', sha256='f1e4ffabc29e6cfe857f627da095be3cfcbe0e1f02ae75e572f10b4a026c5a12')
    version('0.9', 'b42730691eca8fc9a28903c272d11605')
    version('0.8', '06b0404a00e25736946607a36ee5351d')
    version('0.6', '7fa522d2eda97593978021bda9670c0e')

    depends_on('r-htmltools@0.3:', type=('build', 'run'))
    depends_on('r-jsonlite@0.9.16:', type=('build', 'run'))
    depends_on('r-yaml', type=('build', 'run'))
