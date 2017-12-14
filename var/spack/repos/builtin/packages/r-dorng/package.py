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


class RDorng(RPackage):
    """Provides functions to perform reproducible parallel foreach loops,
       using independent random streams as generated by L'Ecuyer's combined
       multiple-recursive generator
       [L'Ecuyer (1999), <doi:10.1287/opre.47.1.159>]. It enables to easily
       convert standard %dopar% loops into fully reproducible loops,
       independently of the number of workers, the task scheduling strategy,
       or the chosen parallel environment and associated foreach backend."""

    homepage = "https://cran.rstudio.com/web/packages/doRNG/index.html"
    url      = "https://cran.rstudio.com/src/contrib/doRNG_1.6.6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/doRNG"

    version('1.6.6', 'ffb26024c58c8c99229470293fbf35cf')

    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-rngtools', type=('build', 'run'))
    depends_on('r-iterators', type=('build', 'run'))
    depends_on('r-pkgmaker', type=('build', 'run'))
