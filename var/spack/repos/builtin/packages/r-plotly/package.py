##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class RPlotly(RPackage):
    """Easily translate 'ggplot2' graphs to an interactive web-based version
    and/or create custom web-based visualizations directly from R."""

    homepage = "https://cran.r-project.org/web/packages/plotly/index.html"
    url      = "https://cran.r-project.org/src/contrib/plotly_4.7.1.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/plotly"

    version('4.7.1', '4799c8b429291d4c52fb904380806548')
    version('4.7.0', '5bd52d515c01af7ff291c30a6cf23bec')
    version('4.6.0', '27ff3de288bacfaad6e6694752ea2929')
    version('4.5.6', 'e6e00177fa64dc6b1a199facfd73f585')
    version('4.5.2', '7eb11b24a9faa9a572657fd89ed72fa5')

    depends_on('r@3.4.0:3.4.9')
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-base64enc', type=('build', 'run'))
    depends_on('r-htmltools', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-htmlwidgets', type=('build', 'run'))
    depends_on('r-data-table', type=('build', 'run'))
    depends_on('r-hexbin', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-crosstalk', type=('build', 'run'))
