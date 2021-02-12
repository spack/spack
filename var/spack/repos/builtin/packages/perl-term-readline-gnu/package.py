# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PerlTermReadlineGnu(PerlPackage):
    """Perl extension for the GNU Readline/History Library."""

    homepage = "https://metacpan.org/pod/Term::ReadLine::Gnu"
    url      = "https://cpan.metacpan.org/authors/id/H/HA/HAYASHI/Term-ReadLine-Gnu-1.36.tar.gz"

    version('1.37', sha256='3bd31a998a9c14748ee553aed3e6b888ec47ff57c07fc5beafb04a38a72f0078')
    version('1.36', sha256='9a08f7a4013c9b865541c10dbba1210779eb9128b961250b746d26702bab6925')

    depends_on('readline')
