# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlIoString(PerlPackage):
    """Emulate file interface for in-core strings"""

    homepage = "http://search.cpan.org/~gaas/IO-String-1.08/String.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/IO-String-1.08.tar.gz"

    version('1.08', '250e5424f290299fc3d6b5d1e9da3835')
