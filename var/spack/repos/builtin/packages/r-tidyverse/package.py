##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class RTidyverse(RPackage):
    """The 'tidyverse' is a set of packages that work in harmony because they
       share common data representations and 'API' design. This package is
       designed to make it easy to install and load multiple 'tidyverse'
       packages in a single step."""

    homepage = "http://tidyverse.tidyverse.org/"
    url      = "https://cran.r-project.org/src/contrib/tidyverse_1.2.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/tidyverse"

    version('1.2.1', '7e2ca0b72ab668342c02fd0f52c082e1')

    depends_on('r-broom@0.4.2:', type=('build', 'run'))
    depends_on('r-cli@1.0.0:', type=('build', 'run'))
    depends_on('r-crayon@1.3.4:', type=('build', 'run'))
    depends_on('r-dplyr@0.7.4:', type=('build', 'run'))
    depends_on('r-dbplyr@1.1.0:', type=('build', 'run'))
    depends_on('r-forcats@0.2.0:', type=('build', 'run'))
    depends_on('r-ggplot2@2.2.1:', type=('build', 'run'))
    depends_on('r-haven@1.1.0:', type=('build', 'run'))
    depends_on('r-hms@0.3:', type=('build', 'run'))
    depends_on('r-httr@1.3.1:', type=('build', 'run'))
    depends_on('r-jsonlite@1.5:', type=('build', 'run'))
    depends_on('r-lubridate@1.7.1:', type=('build', 'run'))
    depends_on('r-magrittr@1.5:', type=('build', 'run'))
    depends_on('r-modelr@0.1.1:', type=('build', 'run'))
    depends_on('r-purrr@0.2.4:', type=('build', 'run'))
    depends_on('r-readr@1.1.1:', type=('build', 'run'))
    depends_on('r-readxl@1.0.0:', type=('build', 'run'))
    depends_on('r-reprex@0.1.1:', type=('build', 'run'))
    depends_on('r-rlang@0.1.4:', type=('build', 'run'))
    depends_on('r-rstudioapi@0.7:', type=('build', 'run'))
    depends_on('r-rvest@0.3.2:', type=('build', 'run'))
    depends_on('r-stringr@1.2.0:', type=('build', 'run'))
    depends_on('r-tibble@1.3.4:', type=('build', 'run'))
    depends_on('r-tidyr@0.7.2:', type=('build', 'run'))
    depends_on('r-xml2@1.1.1:', type=('build', 'run'))
    depends_on('r-rlang@0.1.4:', type=('build', 'run'))
