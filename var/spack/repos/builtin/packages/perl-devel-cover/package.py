# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDevelCover(PerlPackage):
    """Devel::Cover - Perl extension for code coverage metrics"""

    homepage = "https://metacpan.org/pod/Devel::Cover"
    url = "https://cpan.metacpan.org/authors/id/P/PJ/PJCJ/Devel-Cover-1.40.tar.gz"

    version("1.40", sha256="26e2f431fbcf7bff3851f352f83b84067c09ff206f40ab975cad8d2bafe711a8")
