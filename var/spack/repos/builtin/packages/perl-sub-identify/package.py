# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlSubIdentify(PerlPackage):
    """Retrieve names of code references"""

    homepage = "http://search.cpan.org/~rgarcia/Sub-Identify-0.14/lib/Sub/Identify.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RG/RGARCIA/Sub-Identify-0.14.tar.gz"

    version('0.14', '014f19e72698b6a2cbcb54adc9691825')
