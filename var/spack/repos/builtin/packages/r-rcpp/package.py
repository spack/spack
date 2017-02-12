##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class RRcpp(RPackage):
    """The 'Rcpp' package provides R functions as well as C++ classes which
    offer a seamless integration of R and C++. Many R data types and objects
    can be mapped back and forth to C++ equivalents which facilitates both
    writing of new code as well as easier integration of third-party libraries.
    Documentation about 'Rcpp' is provided by several vignettes included in
    this package, via the 'Rcpp Gallery' site at <http://gallery.rcpp.org>, the
    paper by Eddelbuettel and Francois (2011, JSS), and the book by
    Eddelbuettel (2013, Springer); see 'citation("Rcpp")' for details on these
    last two."""

    homepage = "http://dirk.eddelbuettel.com/code/rcpp.html"
    url      = "https://cran.r-project.org/src/contrib/Rcpp_0.12.9.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/Rcpp"

    version('0.12.9', '691c49b12794507288b728ede03668a5')
    version('0.12.6', 'db4280fb0a79cd19be73a662c33b0a8b')
    version('0.12.5', 'f03ec05b4e391cc46e7ce330e82ff5e2')
