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


class RTidyselect(RPackage):
    """A backend for the selecting functions of the 'tidyverse'. It makes it
       easy to implement select-like functions in your own packages in a way
       that is consistent with other 'tidyverse' interfaces for selection."""

    homepage = "https://cran.r-project.org/package=tidyselect"
    url      = "https://cran.r-project.org/src/contrib/tidyselect_0.2.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/tidyselect"

    version('0.2.3', 'c9dbd895ad7ce209bacfad6d19de91c9')

    depends_on('r-glue', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-rlang@0.1:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.0:', type=('build', 'run'))
