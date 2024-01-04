# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlConstant(PerlPackage):
    """constant - Perl pragma to declare constants."""

    homepage = "https://metacpan.org/pod/constant"
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/constant-1.33.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.33", sha256="79965d4130eb576670e27ca0ae6899ef0060c76da48b02b97682166882f1b504")

    depends_on("perl-extutils-makemaker", type="build")
