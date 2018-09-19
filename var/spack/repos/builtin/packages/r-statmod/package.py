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


class RStatmod(RPackage):
    """A collection of algorithms and functions to aid statistical
    modeling. Includes growth curve comparisons, limiting dilution
    analysis (aka ELDA), mixed linear models, heteroscedastic
    regression, inverse-Gaussian probability calculations, Gauss
    quadrature and a secure convergence algorithm for nonlinear
    models. Includes advanced generalized linear model functions
    that implement secure convergence, dispersion modeling and
    Tweedie power-law families."""

    homepage = "https://cran.r-project.org/package=statmod"
    url      = "https://cran.rstudio.com/src/contrib/statmod_1.4.30.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/statmod"

    version('1.4.30', '34e60132ce3df38208f9dc0db0479151')
