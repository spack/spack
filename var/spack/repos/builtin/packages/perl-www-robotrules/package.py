# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlWwwRobotrules(PerlPackage):
    """Database of robots.txt-derived permissions"""

    homepage = "http://deps.cpantesters.org/?module=WWW%3A%3ARobotRules;perl=latest"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/WWW-RobotRules-6.02.tar.gz"

    version('6.02', 'b7186e8b8b3701e70c22abf430742403')

    depends_on('perl-uri', type=('build', 'run'))
