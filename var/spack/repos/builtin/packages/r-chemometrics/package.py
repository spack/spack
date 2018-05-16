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


class RChemometrics(RPackage):
    """R companion to the book "Introduction to Multivariate Statistical Analysis
    in Chemometrics" written by K. Varmuza and P. Filzmoser (2009)."""

    homepage = "https://cran.r-project.org/web/packages/chemometrics/index.html"
    url      = "https://cran.r-project.org/src/contrib/chemometrics_1.4.2.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/chemometrics"

    version('1.4.2', '8137b0ca4004add9cc2ea81d2c54427f')
    version('1.4.1', '1e5a89442bb4a61db0da884eedd74fc2')
    version('1.3.9', '2b619791896db1513ca3d714acb68af3')
    version('1.3.8', '7fad828bd094b5485fbf20bdf7d3d0d1')
    version('1.3.7', 'a9e2f32efb1545421dd96185fd849184')

    depends_on('r@3.4.0:3.4.9')
    depends_on('r-rpart', type=('build', 'run'))
    depends_on('r-mclust', type=('build', 'run'))
    depends_on('r-lars', type=('build', 'run'))
    depends_on('r-robustbase', type=('build', 'run'))
    depends_on('r-e1071', type=('build', 'run'))
    depends_on('r-pls', type=('build', 'run'))
    depends_on('r-som', type=('build', 'run'))
    depends_on('r-pcapp', type=('build', 'run'))
