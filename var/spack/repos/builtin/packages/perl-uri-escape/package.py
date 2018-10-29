# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlUriEscape(PerlPackage):
    """This module provides functions to percent-encode and percent-decode URI
    strings as defined by RFC 3986. Percent-encoding URI's is informally called
    "URI escaping". This is the terminology used by this module, which predates
    the formalization of the terms by the RFC by several years."""

    homepage = "https://metacpan.org/pod/URI::Escape"
    url      = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/URI-1.71.tar.gz"

    version('1.71', '247c3da29a794f72730e01aa5a715daf')

    depends_on('perl-extutils-makemaker', type='build')
