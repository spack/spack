##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Autoconf(AutotoolsPackage):
    """Autoconf -- system configuration part of autotools"""

    homepage = 'https://www.gnu.org/software/autoconf/'
    url      = 'https://ftpmirror.gnu.org/autoconf/autoconf-2.69.tar.gz'

    version('2.69', '82d05e03b93e45f5a39b828dc9c6c29b')
    version('2.62', '6c1f3b3734999035d77da5024aab4fbd')
    version('2.59', 'd4d45eaa1769d45e59dcb131a4af17a0')
    version('2.13', '9de56d4a161a723228220b0f425dc711')

    # Note: m4 is not a pure build-time dependency of autoconf. m4 is
    # needed when autoconf runs, not only when autoconf is built.
    depends_on('m4@1.4.6:', type=('build', 'run'))
    depends_on('perl', type=('build', 'run'))

    build_directory = 'spack-build'

    def patch(self):
        # The full perl shebang might be too long; we have to fix this here
        # because autom4te is called during the build
        filter_file('^#! @PERL@ -w',
                    '#! /usr/bin/env perl',
                    'bin/autom4te.in')

    @run_after('install')
    def filter_sbang(self):
        # We have to do this after install because otherwise the install
        # target will try to rebuild the binaries (filter_file updates the
        # timestamps)

        # Revert sbang, so Spack's sbang hook can fix it up
        filter_file('^#! /usr/bin/env perl',
                    '#! {0} -w'.format(self.spec['perl'].command.path),
                    self.prefix.bin.autom4te,
                    backup=False)

    def _make_executable(self, name):
        return Executable(join_path(self.prefix.bin, name))

    def setup_dependent_package(self, module, dependent_spec):
        # Autoconf is very likely to be a build dependency,
        # so we add the tools it provides to the dependent module
        executables = ['autoconf',
                       'autoheader',
                       'autom4te',
                       'autoreconf',
                       'autoscan',
                       'autoupdate',
                       'ifnames']
        for name in executables:
            setattr(module, name, self._make_executable(name))
