# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHookLexwrap(PerlPackage):
    """Lexically scoped subroutine wrappers."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/karenetheridge/Hook-LexWrap"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Hook-LexWrap-0.26.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.26", sha256="b60bdc5f98f94f9294b06adef82b1d996da192d5f183f9f434b610fd1137ec2d")
    version("0.25", sha256="08ab9af6bd9b4560702d9d994ad9d905af0c2fd24090d1480ff640f137c1430d")

    depends_on("perl@5.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack

