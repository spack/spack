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

import inspect

from spack.directives import extends
from spack.package import PackageBase


class PythonPackage(PackageBase):
    """Specialized class for packages that are built using Python

    This class provides two phases that can be overridden:
    - build
    - install

    They both have sensible defaults and for many packages the only thing
    necessary will be to add dependencies
    """
    phases = ['build', 'install']
    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = 'PythonPackage'

    extends('python')

    def python(self, *args):
        inspect.getmodule(self).python(*args)

    def setup_py(self, *args):
        self.python(self.setup_file(), '--no-user-cfg', *args)

    def setup_file(self, spec, prefix):
        """Returns the name of the setup file to use."""
        return 'setup.py'

    def build_args(self, spec, prefix):
        """Arguments to pass to build."""
        return []

    def build(self, spec, prefix):
        """Build the Python package."""
        self.setup_py('build', *self.build_args())

    def install_args(self, spec, prefix):
        """Arguments to pass to install."""
        return []

    def install(self, spec, prefix):
        """Install the Python package."""
        args = ['--prefix={0}'.format(prefix)] + self.install_args()
        self.setup_py('install', *args)
