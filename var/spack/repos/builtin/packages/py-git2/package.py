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


class PyGit2(PythonPackage):
    """Pygit2 is a set of Python bindings to the libgit2 shared library,
    libgit2 implements the core of Git.
    """

    homepage = "http://www.pygit2.org/"

    version('0.24.1', 'dd98b6a9fded731e36ca5a40484c8545',
        url="https://pypi.python.org/packages/aa/56/84dcce942a48d4b7b970cfb7a779b8db1d904e5ec5f71e7a67a63a23a4e2/pygit2-0.24.1.tar.gz")

    extends('python')
    depends_on('py-setuptools', type='build')
    # Version must match with libgit2
    # See: http://www.pygit2.org/install.html
    depends_on('libgit2@0.24:', when='@0.24:')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-cffi', type=('build', 'run'))

    def setup_environment(self, spack_env, run_env):
        spec = self.spec
        # http://www.pygit2.org/install.html
        spack_env.set('LIBGIT2', spec['libgit2'].prefix)
        spack_env.set('LIBGIT2_LIB', spec['libgit2'].prefix.lib)
