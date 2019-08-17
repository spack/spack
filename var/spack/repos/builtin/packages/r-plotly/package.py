# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPlotly(RPackage):
    """Easily translate 'ggplot2' graphs to an interactive web-based version
    and/or create custom web-based visualizations directly from R."""

    homepage = "https://cloud.r-project.org/package=plotly"
    url      = "https://cloud.r-project.org/src/contrib/plotly_4.7.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/plotly"

    version('4.9.0', sha256='f761148338231f210fd7fe2f8325ffe9cfdaaaeddd7b933b65c44ebb4f85e2cf')
    version('4.8.0', sha256='78f90282c831bbbb675ed4811fb506a98dd05e37251fabd42ebc263c80bae8a6')
    version('4.7.1', '4799c8b429291d4c52fb904380806548')
    version('4.7.0', '5bd52d515c01af7ff291c30a6cf23bec')
    version('4.6.0', '27ff3de288bacfaad6e6694752ea2929')
    version('4.5.6', 'e6e00177fa64dc6b1a199facfd73f585')
    version('4.5.2', '7eb11b24a9faa9a572657fd89ed72fa5')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r-ggplot2@3.0.0:', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-base64enc', type=('build', 'run'))
    depends_on('r-htmltools@0.3.6:', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-htmlwidgets@1.3:', type=('build', 'run'))
    depends_on('r-data-table', type=('build', 'run'))
    depends_on('r-hexbin', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-crosstalk', when='@4.6.0:', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-jsonlite@1.6:', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-viridislite', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-lazyeval@0.2.0:', type=('build', 'run'))
    depends_on('r-rcolorbrewer', when='@4.6.0:', type=('build', 'run'))
    depends_on('r-data-table', when='@4.7.0:', type=('build', 'run'))
    depends_on('r-rlang', when='@4.8.0:', type=('build', 'run'))
    depends_on('r-promises', when='@4.8.0:', type=('build', 'run'))
