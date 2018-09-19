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


class RFormatr(RPackage):
    """Provides a function tidy_source() to format R source code. Spaces and
    indent will be added to the code automatically, and comments will be
    preserved under certain conditions, so that R code will be more
    human-readable and tidy. There is also a Shiny app as a user interface in
    this package."""

    homepage = "https://cran.r-project.org/package=formatR"
    url      = "https://cran.r-project.org/src/contrib/formatR_1.5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/formatR"

    version('1.5', 'ac735515b8e4c32097154f1b68c5ecc7')
    version('1.4', '98b9b64b2785b35f9df403e1aab6c73c')

    depends_on('r-codetools', type=('build', 'run'))
    depends_on('r-shiny', type=('build', 'run'))
    depends_on('r-testit', type=('build', 'run'))
    # depends_on('r-knitr', type=('build', 'run')) - mutual dependency
