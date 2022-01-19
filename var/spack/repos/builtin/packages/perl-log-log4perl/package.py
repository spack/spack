# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlLogLog4perl(PerlPackage):
    """Log4j implementation for Perl"""

    homepage = "https://metacpan.org/pod/Log::Log4perl"
    url      = "https://cpan.metacpan.org/authors/id/M/MS/MSCHILLI/Log-Log4perl-1.46.tar.gz"

    version('1.46', sha256='31011a17c04e78016e73eaa4865d0481d2ffc3dc22813c61065d90ad73c64e6f')
