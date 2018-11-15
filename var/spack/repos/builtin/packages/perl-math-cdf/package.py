# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlMathCdf(PerlPackage):
    """Generate probabilities and quantiles from several statistical
       probability functions"""

    homepage = "http://search.cpan.org/~callahan/Math-CDF-0.1/CDF.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/C/CA/CALLAHAN/Math-CDF-0.1.tar.gz"

    version('0.1', '7866c7b6b9d27f0ce4b7637334478ab7')
