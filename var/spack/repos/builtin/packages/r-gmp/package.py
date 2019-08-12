# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGmp(RPackage):
    """Multiple Precision Arithmetic (big integers and rationals, prime
       number tests, matrix computation), "arithmetic without limitations"
       using the C library GMP (GNU Multiple Precision Arithmetic)."""

    homepage = "http://mulcyber.toulouse.inra.fr/projects/gmp"
    url      = "https://cran.r-project.org/src/contrib/gmp_0.5-13.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/gmp"

    version('0.5-13.1', '4a45d45e53bf7140720bd44f10b075ed')

    depends_on('gmp@4.2.3:')
