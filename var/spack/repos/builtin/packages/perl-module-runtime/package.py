# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlModuleRuntime(PerlPackage):
    """Runtime module handling"""

    homepage = "http://search.cpan.org/~zefram/Module-Runtime/lib/Module/Runtime.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/Z/ZE/ZEFRAM/Module-Runtime-0.016.tar.gz"

    version('0.016', 'd3d47222fa2e3dfcb4526f6cc8437b20')

    depends_on('perl-module-build', type='build')
