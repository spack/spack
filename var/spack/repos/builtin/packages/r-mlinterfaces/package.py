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


class RMlinterfaces(RPackage):
    """This package provides uniform interfaces to machine learning
    code for data in R and Bioconductor containers."""

    homepage = "https://www.bioconductor.org/packages/MLInterfaces/"
    git      = "https://git.bioconductor.org/packages/MLInterfaces.git"

    version('1.56.0', commit='31fe6fb20d859fcb01d5552f42bca6bab16cc67f')

    depends_on('r@3.4.0:3.4.9', when='@1.56.0')
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-gdata', type=('build', 'run'))
    depends_on('r-pls', type=('build', 'run'))
    depends_on('r-sfsmisc', type=('build', 'run'))
    depends_on('r-rda', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-fpc', type=('build', 'run'))
    depends_on('r-ggvis', type=('build', 'run'))
    depends_on('r-shiny', type=('build', 'run'))
    depends_on('r-gbm', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-hwriter', type=('build', 'run'))
    depends_on('r-threejs', type=('build', 'run'))
    depends_on('r-mlbench', type=('build', 'run'))
