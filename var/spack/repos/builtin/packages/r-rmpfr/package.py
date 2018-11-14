# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRmpfr(RPackage):
    """Arithmetic (via S4 classes and methods) for arbitrary precision
       floating point numbers, including transcendental ("special")
       functions. To this end, Rmpfr interfaces to the LGPL'ed MPFR
       (Multiple Precision Floating-Point Reliable) Library which itself
       is based on the GMP (GNU Multiple Precision) Library."""

    homepage = "http://rmpfr.r-forge.r-project.org"
    url      = "https://cran.r-project.org/src/contrib/Rmpfr_0.6-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/Rmpfr"

    version('0.6-1', '55d4ec257bd2a9233bafee9e444d0265')

    depends_on('r-gmp@0.5-8:', type=('build', 'run'))
    depends_on('mpfr@3.0.0:')
