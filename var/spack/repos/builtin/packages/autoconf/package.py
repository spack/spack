##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
    url = 'http://ftp.gnu.org/gnu/autoconf/autoconf-2.69.tar.gz'

    version('2.69', '82d05e03b93e45f5a39b828dc9c6c29b')
    version('2.62', '6c1f3b3734999035d77da5024aab4fbd')
    version('2.59', 'd4d45eaa1769d45e59dcb131a4af17a0')
    version('2.13', '9de56d4a161a723228220b0f425dc711')

    depends_on('m4@1.4.6:',   type='build')

    build_directory = 'spack-build'

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
