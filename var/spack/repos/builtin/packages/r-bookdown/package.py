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


class RBookdown(RPackage):
    """Output formats and utilities for authoring books and technical
    documents with R Markdown."""

    homepage = "https://cran.r-project.org/package=bookdown"
    url      = "https://cran.rstudio.com/src/contrib/bookdown_0.5.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/bookdown"

    version('0.5', '7bad360948e2b22d28397870b9319f17')

    depends_on('r-yaml@2.1.14:', type=('build', 'run'))
    depends_on('r-rmarkdown@1.5:', type=('build', 'run'))
    depends_on('r-knitr@1.16:', type=('build', 'run'))
    depends_on('r-htmltools@0.3.6:', type=('build', 'run'))
