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


class RSdmtools(RPackage):
    """Species Distribution Modelling Tools: Tools for processing data
    associated with species distribution modelling exercises

    This packages provides a set of tools for post processing the outcomes of
    species distribution modeling exercises."""

    homepage = "https://cran.r-project.org/web/packages/SDMTools/index.html"
    url      = "https://cran.r-project.org/src/contrib/SDMTools_1.1-221.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/SDMTools"

    version('1.1-221', '3604da1783d0c6081b62b29d35a32c3c')
    version('1.1-20', '27cc8de63cfdd86d4ba9983012121c58')
    version('1.1-13', '0d6a14d985988a81b9ff06c635675143')
    version('1.1-12', 'a13d75e4024d908a57ea462112d8a437')
    version('1.1-11', 'cb890ee06eb862f97141b73c7390a0a9')

    depends_on('r@3.4.0:3.4.9')
    depends_on('r-utils', type=('build', 'run'))
