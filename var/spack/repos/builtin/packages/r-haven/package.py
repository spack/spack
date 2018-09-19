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


class RHaven(RPackage):
    """Import foreign statistical formats into R via the embedded 'ReadStat' C
       library, <https://github.com/WizardMac/ReadStat>."""

    homepage = "http://haven.tidyverse.org/"
    url      = "https://cran.r-project.org/src/contrib/haven_1.1.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/haven"

    version('1.1.0', '8edd4b7683f8c36b5bb68582ac1b8733')

    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-readr', type=('build', 'run'))
    depends_on('r-hms', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-forcats', type=('build', 'run'))
