##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
#
from spack import *


class PyPsyclone(PythonPackage):
    """Code generation for the PSyKAl framework from the GungHo project,
       as used by the LFRic model at the UK Met Office."""

    homepage = "https://github.com/stfc/PSyclone"
    url      = "https://github.com/stfc/PSyclone/archive/1.5.1.tar.gz"
    git      = "https://github.com/stfc/PSyclone.git"

    version('develop', branch='master')
    version('1.5.1', commit='eba7a097175b02f75dec70616cf267b7b3170d78')

    depends_on('py-setuptools', type='build')
    depends_on('py-pyparsing', type=('build', 'run'))

    # Test cases fail without compatible versions of py-fparser:
    depends_on('py-fparser@0.0.5', type=('build', 'run'), when='@1.5.1')
    depends_on('py-fparser', type=('build', 'run'), when='@1.5.2:')

    # Dependencies only required for tests:
    depends_on('py-numpy',  type='test')
    depends_on('py-nose',   type='test')
    depends_on('py-pytest', type='test')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_build(self):
        # Limit py.test to search inside the build tree:
        touch('pytest.ini')
        with working_dir('src'):
            Executable('py.test')()

    def setup_environment(self, spack_env, run_env):
        # Allow testing with installed executables:
        spack_env.prepend_path('PATH', self.prefix.bin)
