# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlIoHtml(PerlPackage):
    """Open an HTML file with automatic charset detection."""

    homepage = "http://search.cpan.org/~cjm/IO-HTML-1.001/lib/IO/HTML.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/C/CJ/CJM/IO-HTML-1.001.tar.gz"

    version('1.001', '3f8958718844dc96b9f6946f21d70d22')
