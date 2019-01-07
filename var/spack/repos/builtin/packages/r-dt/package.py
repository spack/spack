# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDt(RPackage):
    """Data objects in R can be rendered as HTML tables using the JavaScript
    library 'DataTables' (typically via R Markdown or Shiny). The 'DataTables'
    library has been included in this R package. The package name 'DT' is an
    abbreviation of 'DataTables'."""

    homepage = "http://rstudio.github.io/DT"
    url      = "https://cran.r-project.org/src/contrib/DT_0.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/DT"

    version('0.4', sha256='3daa96b819ca54e5fbc2c7d78cb3637982a2d44be58cea0683663b71cfc7fa19')
    version('0.3', sha256='ef42b24c9ea6cfa1ce089687bf858d773ac495dc80756d4475234e979bd437eb')
    version('0.2', sha256='a1b7f9e5c31a241fdf78ac582499f346e915ff948554980bbc2262c924b806bd')
    version('0.1', sha256='129bdafededbdcc3279d63b16f00c885b215f23cab2edfe33c9cbe177c8c4756')

    depends_on('r-htmltools@0.3.6:', type=('build', 'run'))
    depends_on('r-htmlwidgets@1.3:', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-crosstalk', type=('build', 'run'))
