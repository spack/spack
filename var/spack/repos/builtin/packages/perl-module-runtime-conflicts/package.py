# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlModuleRuntimeConflicts(PerlPackage):
    """Provide information on conflicts for Module::Runtime"""

    homepage = "http://search.cpan.org/~ether/Module-Runtime-Conflicts-0.003/lib/Module/Runtime/Conflicts.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Module-Runtime-Conflicts-0.003.tar.gz"

    version('0.003', '67aaf699072063cc00c5b6afd4c67a6f')
