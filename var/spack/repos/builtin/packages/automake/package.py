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


class Automake(AutotoolsPackage):
    """Automake -- make file builder part of autotools"""

    homepage = 'http://www.gnu.org/software/automake/'
    url      = 'https://ftpmirror.gnu.org/automake/automake-1.15.tar.gz'

    version('1.16.1', '83cc2463a4080efd46a72ba2c9f6b8f5')
    version('1.15.1', '95df3f2d6eb8f81e70b8cb63a93c8853')
    version('1.15',   '716946a105ca228ab545fc37a70df3a3')
    version('1.14.1', 'd052a3e884631b9c7892f2efce542d75')
    version('1.11.6', '0286dc30295b62985ca51919202ecfcc')

    depends_on('autoconf', type='build')
    depends_on('perl', type=('build', 'run'))

    build_directory = 'spack-build'

    def patch(self):
        # The full perl shebang might be too long
        files_to_be_patched_fmt = 'bin/{0}.in'
        if '@:1.15.1' in self.spec:
            files_to_be_patched_fmt = 't/wrap/{0}.in'

        for file in ('aclocal', 'automake'):
            filter_file('^#!@PERL@ -w',
                        '#!/usr/bin/env perl',
                        files_to_be_patched_fmt.format(file))

    def _make_executable(self, name):
        return Executable(join_path(self.prefix.bin, name))

    def setup_dependent_package(self, module, dependent_spec):
        # Automake is very likely to be a build dependency,
        # so we add the tools it provides to the dependent module
        executables = ['aclocal', 'automake']
        for name in executables:
            setattr(module, name, self._make_executable(name))
