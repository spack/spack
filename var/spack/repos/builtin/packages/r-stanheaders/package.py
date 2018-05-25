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


class RStanheaders(RPackage):
    """The C++ header files of the Stan project are provided by this package,
    but it contains no R code, vignettes, or function documentation. There is a
    shared object containing part of the CVODES library, but it is not
    accessible from R. StanHeaders is only useful for developers who want to
    utilize the LinkingTo directive of their package's DESCRIPTION file to
    build on the Stan library without incurring unnecessary dependencies. The
    Stan project develops a probabilistic programming language that implements
    full or approximate Bayesian statistical inference via Markov Chain Monte
    Carlo or variational methods and implements (optionally penalized) maximum
    likelihood estimation via optimization. The Stan library includes an
    advanced automatic differentiation scheme, templated statistical and linear
    algebra functions that can handle the automatically differentiable scalar
    types (and doubles, ints, etc.), and a parser for the Stan language. The
    'rstan' package provides user-facing R functions to parse, compile, test,
    estimate, and analyze Stan models."""

    homepage = "http://mc-stan.org/"
    url      = "https://cran.r-project.org/src/contrib/StanHeaders_2.10.0-2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/StanHeaders"

    version('2.17.1', '11d8770277dd18e563852852633c6c25')
    version('2.10.0-2', '9d09b1e9278f08768f7a988ad9082d57')
