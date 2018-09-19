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


class RBiocstyle(RPackage):
    """Provides standard formatting styles for Bioconductor PDF and HTML
    documents. Package vignettes illustrate use and functionality."""

    homepage = "https://www.bioconductor.org/packages/BiocStyle/"
    git      = "https://git.bioconductor.org/packages/BiocStyle.git"

    version('2.4.1', commit='ef10764b68ac23a3a7a8ec3b6a6436187309c138')

    depends_on('r-bookdown', type=('build', 'run'))
    depends_on('r-knitr@1.12:', type=('build', 'run'))
    depends_on('r-rmarkdown@1.2:', type=('build', 'run'))
    depends_on('r-yaml', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.4.1')
