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


class RNor1mix(RPackage):
    """Onedimensional Normal Mixture Models Classes, for, e.g., density
       estimation or clustering algorithms research and teaching; providing
       the widely used Marron-Wand densities. Efficient random number
       generation and graphics; now fitting to data by ML (Maximum Likelihood)
       or EM estimation."""

    homepage = "https://CRAN.R-project.org/package=nor1mix"
    url      = "https://cran.rstudio.com/src/contrib/nor1mix_1.2-3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/nor1mix"

    version('1.2-3', '60eb5cc1ea6b366f53042087a080b105')
