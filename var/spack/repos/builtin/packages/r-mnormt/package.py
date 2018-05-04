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


class RMnormt(RPackage):
    """Functions are provided for computing the density and the distribution
       function of multivariate normal and "t" random variables, and for
       generating random vectors sampled from these distributions.
       Probabilities are computed via non-Monte Carlo methods; different
       routines are used in the case d=1, d=2, d>2, if d denotes the number
       of dimensions."""

    homepage = "http://azzalini.stat.unipd.it/SW/Pkg-mnormt"
    url      = "https://cran.r-project.org/src/contrib/mnormt_1.5-5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/mnormt"

    version('1.5-5', '19b5be2e9ed33b92d7a716bfcca6b2c7')
