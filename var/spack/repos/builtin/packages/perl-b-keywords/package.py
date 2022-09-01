# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlBKeywords(PerlPackage):
    """Lists of reserved barewords and symbol names."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/R/RU/RURBAN"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/R/RU/RURBAN/B-Keywords-1.24.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.24", sha256="a5cf6bb285d06d17cee227783b723bb274213fd4153a5dee311d240e1169606e")
    version("1.23", sha256="13689a4c4273c0b9b4aa855764b34b7ad8bf7da1451b7468a5cef82f677b3aaa")

    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack

