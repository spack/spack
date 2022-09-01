# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileFindRulePerl(PerlPackage):
    """Common rules for searching for Perl things."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/karenetheridge/File-Find-Rule-Perl"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/File-Find-Rule-Perl-1.16.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.16", sha256="ae1886050d9ca21223c073e2870abdc80dc30e3f55289a11c37da3820a8321ff")
    version("1.15", sha256="9a48433f86e08ce18e03526e2982de52162eb909d19735460f07eefcaf463ea6")

    depends_on("perl-params-util@0.38:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-file-find-rule@0.20:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack

