##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Libtool(AutotoolsPackage):
    """libtool -- library building part of autotools."""

    homepage = 'https://www.gnu.org/software/libtool/'
    url = 'http://ftpmirror.gnu.org/libtool/libtool-2.4.2.tar.gz'

    version('2.4.6', 'addf44b646ddb4e3919805aa88fa7c5e')
    version('2.4.2', 'd2f3b7d4627e69e13514a40e72a24d50')

    depends_on('m4@1.4.6:', type='build')

    build_directory = 'spack-build'

    def _make_executable(self, name):
        return Executable(join_path(self.prefix.bin, name))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.append_path('ACLOCAL_PATH',
                              join_path(self.prefix.share, 'aclocal'))

    def setup_dependent_package(self, module, dependent_spec):
        # Automake is very likely to be a build dependency,
        # so we add the tools it provides to the dependent module
        executables = ['libtoolize', 'libtool']
        for name in executables:
            setattr(module, name, self._make_executable(name))
