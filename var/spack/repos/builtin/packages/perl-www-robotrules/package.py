# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlWwwRobotrules(PerlPackage):
    """Database of robots.txt-derived permissions"""

    homepage = "http://deps.cpantesters.org/?module=WWW%3A%3ARobotRules;perl=latest"
    url = "https://cpan.metacpan.org/authors/id/G/GA/GAAS/WWW-RobotRules-6.02.tar.gz"

    version("6.02", sha256="46b502e7a288d559429891eeb5d979461dd3ecc6a5c491ead85d165b6e03a51e")

    provides("perl-www-robotrules-anydbm-file@6.00")  # AUTO-CPAN2Spack
    provides("perl-www-robotrules-incore")  # AUTO-CPAN2Spack
    depends_on("perl@5.8.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-uri@1.10:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
