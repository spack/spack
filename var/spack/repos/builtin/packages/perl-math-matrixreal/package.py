# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlMathMatrixreal(PerlPackage):
    """Implements the data type "matrix of real numbers" (and consequently
    also "vector of real numbers")."""

    homepage = "http://search.cpan.org/~leto/Math-MatrixReal/lib/Math/MatrixReal.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/L/LE/LETO/Math-MatrixReal-2.13.tar.gz"

    version('2.13', 'cf9d6ff71f2df075559ea752104ca199')

    depends_on('perl-module-build', type='build')
