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


class RAnaquin(RPackage):
    """The project is intended to support the use of sequins
    (synthetic sequencing spike-in controls) owned and made available
    by the Garvan Institute of Medical Research. The goal is to
    provide a standard open source library for quantitative analysis,
    modelling and visualization of spike-in controls."""

    homepage = "https://www.bioconductor.org/packages/Anaquin/"
    git      = "https://git.bioconductor.org/packages/Anaquin.git"

    version('1.2.0', commit='584d1970cc9dc1d354f9a6d7c1306bd7e8567119')

    depends_on('r@3.4.0:3.4.9', when='@1.2.0')
    depends_on('r-deseq2', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-locfit', type=('build', 'run'))
    depends_on('r-qvalue', type=('build', 'run'))
    depends_on('r-knitr', type=('build', 'run'))
    depends_on('r-rocr', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
