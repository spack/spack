# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlAttributeHandlers(PerlPackage):
    """Simpler definition of attribute handlers."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Attribute-Handlers-0.99.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("0.99", sha256="937ea3ebfc9b14f4a4148bf3c32803709edbd12a387137a26370b38ee1fc9835")
    version("0.98", sha256="7d53613496faf6f25c41dfb870b3aca197ed7208252b6b4fd7a39a57511d401a")

    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack

