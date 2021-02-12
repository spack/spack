# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlLogLog4perl(PerlPackage):
    """Log4j implementation for Perl"""

    homepage = "http://search.cpan.org/~mschilli/Log-Log4perl-1.44/lib/Log/Log4perl.pm"
    url      = "https://cpan.metacpan.org/authors/id/M/MS/MSCHILLI/Log-Log4perl-1.46.tar.gz"

    version('1.49', sha256='b739187f519146cb6bebcfc427c64b1f4138b35c5f4c96f46a21ed4a43872e16')
    version('1.48', sha256='cf6e9fc1f9183fabbe540d84f603c6541458034092b7c53e41008093db62dc98')
    version('1.47', sha256='9001dded011226538b9a50c7856815bb0dba72a1e6218fdcaba56f651356b96f')
    version('1.46', sha256='31011a17c04e78016e73eaa4865d0481d2ffc3dc22813c61065d90ad73c64e6f')
