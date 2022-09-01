# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDigestMd5(PerlPackage):
    """Perl interface to the MD5 Algorithm"""

    homepage = "https://metacpan.org/pod/Digest::MD5"
    url = "https://cpan.metacpan.org/authors/id/T/TO/TODDR/Digest-MD5-2.58.tar.gz"

    version("2.58", sha256="7d0201977a76ad390a7fbcce1f159278599dcb34de123246bea0c6338dd7f714")
    version("2.57", sha256="1221bc1894feca0844b3a2d94263e98609fe4fa86b6247c664c59bd0bee5a711")
    version("2.56", sha256="0ec5a604999bad344e13c6c76e09814c7daab001a338aeef2501cb5c1f83dd7f")

    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
