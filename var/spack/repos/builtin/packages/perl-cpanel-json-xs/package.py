# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCpanelJsonXs(PerlPackage):
    """CPanel fork of JSON::XS, fast and correct serializing."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/R/RU/RURBAN"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/R/RU/RURBAN/Cpanel-JSON-XS-4.32.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("4.32", sha256="ece9d35914175e6c47b62fd936244278365ebce0905fe92b037e484e6d501895")
    version("4.31", sha256="02a67acee3de24a728c396486800e2a235591a543d0794449ad388fe3d5cff29")

    provides("perl-cpanel-json-xs-type")  # AUTO-CPAN2Spack
    depends_on("perl-math-bigint", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-math-bigfloat@1.16:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-time-piece", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-data-dumper", type=("build", "test"))  # AUTO-CPAN2Spack

