# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RRcppgsl(RPackage):
    """'Rcpp' Integration for 'GNU GSL' Vectors and Matrices.

    'Rcpp' integration for 'GNU GSL' vectors and matrices The 'GNU Scientific
    Library' (or 'GSL') is a collection of numerical routines for scientific
    computing. It is particularly useful for C and C++ programs as it provides
    a standard C interface to a wide range of mathematical routines. There are
    over 1000 functions in total with an extensive test suite. The 'RcppGSL'
    package provides an easy-to-use interface between 'GSL' data structures and
    R using concepts from 'Rcpp' which is itself a package that eases the
    interfaces between R and C++. This package also serves as a prime example
    of how to build a package that uses 'Rcpp' to connect to another
    third-party library. The 'autoconf' script, 'inline' plugin and example
    package can all be used as a stanza to write a similar package against
    another library."""

    cran = "RcppGSL"

    version('0.3.10', sha256='8612087da02fb791f427fed310c23d0482a8eb60fb089119f018878143f95451')

    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
    depends_on('gsl')
