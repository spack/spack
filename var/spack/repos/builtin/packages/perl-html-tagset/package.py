# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlHtmlTagset(PerlPackage):
    """Data tables useful in parsing HTML"""

    homepage = "http://search.cpan.org/~petdance/HTML-Tagset-3.20/Tagset.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/P/PE/PETDANCE/HTML-Tagset-3.20.tar.gz"

    version('3.20', 'd2bfa18fe1904df7f683e96611e87437')
