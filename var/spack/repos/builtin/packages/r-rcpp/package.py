# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
    url      = "https://cloud.r-project.org/src/contrib/Rcpp_0.12.13.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Rcpp"

    version('1.0.2', sha256='ad9338d6fc89dd116a3e2c5ecef1956e4be63b6c6aa1b21b2e5f249d65a5129c')
    version('1.0.0',   sha256='b7378bf0dda17ef72aa3f2a318a9cb5667bef50b601dc1096431e17426e18bc2')
    version('0.12.19', sha256='63aeb6d4b58cd2899ded26f38a77d461397d5b0dc5936f187d3ca6cd958ab582')
    version('0.12.18', sha256='fcecd01e53cfcbcf58dec19842b7235a917b8d98988e4003cc090478c5bbd300')
    version('0.12.17', sha256='4227c45c92416b5378ed5761495f9b3932d481bae9a190fb584d17c10744af23')
    version('0.12.16', 'ab5107766c63d66065ed1a92a4cab1b7')
    version('0.12.15', 'bebac0782862c15c2944764343e55582')
    version('0.12.14', '89a3dbad0aa3e345b9d0b862fa1fc56a')
    version('0.12.13', '5186d119132bfe07f66da74c50b190a4')
    version('0.12.12', '97b36a3b567e3438067c4a7d0075fd90')
    version('0.12.11', 'ea1710213cbb1d91b1d0318e6fa9aa37')
    version('0.12.9', '691c49b12794507288b728ede03668a5')
    version('0.12.6', 'db4280fb0a79cd19be73a662c33b0a8b')
    version('0.12.5', 'f03ec05b4e391cc46e7ce330e82ff5e2')

    depends_on('r@3.0.0:', type=('build', 'run'))
