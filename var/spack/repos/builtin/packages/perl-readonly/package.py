# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlReadonly(PerlPackage):
    """Readonly - Facility for creating read-only scalars, arrays, hashes"""

    homepage = "https://metacpan.org/pod/Readonly"
    url      = "https://cpan.metacpan.org/authors/id/S/SA/SANKO/Readonly-2.05.tar.gz"

    version('2.05', sha256='4b23542491af010d44a5c7c861244738acc74ababae6b8838d354dfb19462b5e')

    depends_on('perl-module-build-tiny', type='build')

    # The following is needed to work around #12852
    @run_after('configure')
    def fix_shebang(self):
        pattern = '#!{0}'.format(self.spec['perl'].command.path)
        repl = '#!/usr/bin/env perl'
        filter_file(pattern, repl, 'Build', backup=False)
