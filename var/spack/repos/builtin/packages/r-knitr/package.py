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


class RKnitr(RPackage):
    """Provides a general-purpose tool for dynamic report generation in R using
    Literate Programming techniques."""

    homepage = "https://cran.r-project.org/package=knitr"
    url      = "https://cran.rstudio.com/src/contrib/knitr_1.14.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/knitr"

    version('1.17', '4407ccf8f2a51629800d6d5243cf3e70')
    version('1.14', 'ef0fbeaa9372f99ffbc57212a7781511')
    version('0.6',  'c67d6db84cd55594a9e870c90651a3db')

    depends_on('r-evaluate', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-formatr', type=('build', 'run'))
    depends_on('r-highr', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-markdown', type=('build', 'run'))
    depends_on('r-yaml', type=('build', 'run'))
