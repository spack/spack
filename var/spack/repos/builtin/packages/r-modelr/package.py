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


class RModelr(RPackage):
    """Functions for modelling that help you seamlessly integrate modelling
       into a pipeline of data manipulation and visualisation."""

    homepage = "https://github.com/hadley/modelr"
    url      = "https://cran.r-project.org/src/contrib/modelr_0.1.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/modelr"

    version('0.1.1', 'ce5fd088fb7850228ab1e34d241a975d')

    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-lazyeval', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-broom', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))
