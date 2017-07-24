##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class RRmarkdown(RPackage):
    """Convert R Markdown documents into a variety of formats."""

    homepage = "http://rmarkdown.rstudio.com/"
    url      = "https://cran.r-project.org/src/contrib/rmarkdown_1.6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/rmarkdown"

    version('1.6', '8273346f8a362d6ecbf5da075e066fe1')
    version('1.0', '264aa6a59e9680109e38df8270e14c58')

    depends_on('r@3.0:', type=('build', 'run'))

    depends_on('r-knitr@1.14:', type=('build', 'run'))
    depends_on('r-yaml@2.1.5:', type=('build', 'run'))
    depends_on('r-htmltools@0.3.5:', type=('build', 'run'))
    depends_on('r-catools', type=('build', 'run'))
    depends_on('r-evaluate@0.8:', type=('build', 'run'))
    depends_on('r-base64enc', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-rprojroot', when='@1.6:', type=('build', 'run'))
    depends_on('r-stringr@1.2.0:', when='@1.6:', type=('build', 'run'))
