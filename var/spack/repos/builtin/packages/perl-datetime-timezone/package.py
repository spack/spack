# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDatetimeTimezone(PerlPackage):
    """DateTime::TimeZone - Time zone object base class and factory"""

    homepage = "https://metacpan.org/pod/DateTime::TimeZone"
    url = "https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/DateTime-TimeZone-2.60.tar.gz"

    version("2.60", sha256="f0460d379323905b579bed44e141237a337dc25dd26b6ab0c60ac2b80629323d")
