# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlMinimumversion(PerlPackage):
    """Find a minimum required version of perl for Perl code."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/neilb/Perl-MinimumVersion"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/D/DB/DBOOK/Perl-MinimumVersion-1.40.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.40", sha256="7589a578cb60d70ca4755c395b3592b440a0cd6a1b074e4eceac93b031a1be90")
    version("1.39-TRIAL", sha256="df936dbacd2dcf2850fae49a3cb766fa3364f8138a05eba0c7da43b63744d5e7")

    provides("perl-perl-minimumversion-reason")  # AUTO-CPAN2Spack
    depends_on("perl-params-util@0.25:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-file-find-rule-perl", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-file-find-rule", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppix-regexp@0.33:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-ppi@1.215:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppi-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ppix-utils", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-list-util@1.20:", type="run")  # AUTO-CPAN2Spack

