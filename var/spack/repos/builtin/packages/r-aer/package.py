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


class RAer(RPackage):
    """Functions, data sets, examples, demos, and vignettes
    for the book Christian Kleiber and Achim Zeileis (2008),
    Applied Econometrics with R, Springer-Verlag, New York.
    ISBN 978-0-387-77316-2."""

    homepage = "https://cran.r-project.org/web/packages/AER/index.html"
    url      = "https://cran.r-project.org/src/contrib/AER_1.2-5.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/AER"

    version('1.2-5', '419df9dc8ee6e5edd79678fee06719ae')

    depends_on('r@2.13.0:', type=('build', 'run'))
    depends_on('r-car@2.10-19:', type=('build', 'run'))
    depends_on('r-lmtest', type=('build', 'run'))
    depends_on('r-sandwich', type=('build', 'run'))
    depends_on('r-survival@2.37-5:', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-formula', type=('build', 'run'))
