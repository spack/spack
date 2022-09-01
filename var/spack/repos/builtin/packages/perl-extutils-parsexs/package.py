# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExtutilsParsexs(PerlPackage):
    """Converts Perl XS code into C code."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/Perl/perl5"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/X/XS/XSAWYERX/ExtUtils-ParseXS-3.44.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("3.44", sha256="77effdf31af36ef656f09aa7c15356d238dab6d1afaa7278ae15c1b6bcf86266")

    provides("perl-extutils-parsexs-constants")  # AUTO-CPAN2Spack
    provides("perl-extutils-parsexs-countlines")  # AUTO-CPAN2Spack
    provides("perl-extutils-parsexs-eval")  # AUTO-CPAN2Spack
    provides("perl-extutils-parsexs-utilities")  # AUTO-CPAN2Spack
    provides("perl-extutils-typemaps")  # AUTO-CPAN2Spack
    provides("perl-extutils-typemaps-cmd")  # AUTO-CPAN2Spack
    provides("perl-extutils-typemaps-inputmap")  # AUTO-CPAN2Spack
    provides("perl-extutils-typemaps-outputmap")  # AUTO-CPAN2Spack
    provides("perl-extutils-typemaps-type")  # AUTO-CPAN2Spack
    depends_on("perl-dynaloader", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.46:", type=("build", "run"))  # AUTO-CPAN2Spack

