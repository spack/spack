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
    # Default phases
    phases = ['build', 'install']

    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = 'PythonPackage'

    extends('python')

    # If True, `--no-user-cfg` is passed to setup.py
    # ignore pydistutils.cfg in your home directory
    no_user_cfg = True

    def python(self, *args):
        inspect.getmodule(self).python(*args)

    def setup_py(self, *args):
        setup = self.setup_file(self.spec, self.prefix)
        if self.no_user_cfg:
            self.python(setup, '--no-user-cfg', *args)
        else:
            self.python(setup, *args)

    def setup_file(self, spec, prefix):
        """Returns the name of the setup file to use."""
        return 'setup.py'

    # The following phases and their descriptions come from:
    #   $ python setup.py --help-commands
    # Only standard commands are included here, but some packages
    # define extra commands as well

    def build(self, spec, prefix):
        """Build everything needed to install."""
        args = self.build_args(spec, prefix)

        self.setup_py('build', *args)

    def build_args(self, spec, prefix):
        """Arguments to pass to build."""
        return []

    def build_py(self, spec, prefix):
        '''"Build" pure Python modules (copy to build directory).'''
        args = self.build_py_args(spec, prefix)

        self.setup_py('build_py', *args)

    def build_py_args(self, spec, prefix):
        """Arguments to pass to build_py."""
        return []

    def build_ext(self, spec, prefix):
        """Build C/C++ extensions (compile/link to build directory)."""
        args = self.build_ext_args(spec, prefix)

        self.setup_py('build_ext', *args)

    def build_ext_args(self, spec, prefix):
        """Arguments to pass to build_ext."""
        return []

    def build_clib(self, spec, prefix):
        """Build C/C++ libraries used by Python extensions."""
        args = self.build_clib_args(spec, prefix)

        self.setup_py('build_clib', *args)

    def build_clib_args(self, spec, prefix):
        """Arguments to pass to build_clib."""
        return []

    def build_scripts(self, spec, prefix):
        '''"Build" scripts (copy and fixup #! line).'''
        args = self.build_scripts_args(spec, prefix)

        self.setup_py('build_scripts', *args)

    def clean(self, spec, prefix):
        """Clean up temporary files from 'build' command."""
        args = self.clean_args(spec, prefix)

        self.setup_py('clean', *args)

    def clean_args(self, spec, prefix):
        """Arguments to pass to clean."""
        return []

    def install(self, spec, prefix):
        """Install everything from build directory."""
        args = self.install_args(spec, prefix)

        self.setup_py('install', *args)

    def install_args(self, spec, prefix):
        """Arguments to pass to install."""
        return ['--prefix={0}'.format(prefix)]

    def install_lib(self, spec, prefix):
        """Install all Python modules (extensions and pure Python)."""
        args = self.install_lib_args(spec, prefix)

        self.setup_py('install_lib', *args)

    def install_lib_args(self, spec, prefix):
        """Arguments to pass to install_lib."""
        return []

    def install_headers(self, spec, prefix):
        """Install C/C++ header files."""
        args = self.install_headers_args(spec, prefix)

        self.setup_py('install_headers', *args)

    def install_headers_args(self, spec, prefix):
        """Arguments to pass to install_headers."""
        return []

    def install_scripts(self, spec, prefix):
        """Install scripts (Python or otherwise)."""
        args = self.install_scripts_args(spec, prefix)

        self.setup_py('install_scripts', *args)

    def install_scripts_args(self, spec, prefix):
        """Arguments to pass to install_scripts."""
        return []

    def install_data(self, spec, prefix):
        """Install data files."""
        args = self.install_data_args(spec, prefix)

        self.setup_py('install_data', *args)

    def install_data_args(self, spec, prefix):
        """Arguments to pass to install_data."""
        return []

    def sdist(self, spec, prefix):
        """Create a source distribution (tarball, zip file, etc.)."""
        args = self.sdist_args(spec, prefix)

        self.setup_py('sdist', *args)

    def sdist_args(self, spec, prefix):
        """Arguments to pass to sdist."""
        return []

    def register(self, spec, prefix):
        """Register the distribution with the Python package index."""
        args = self.register_args(spec, prefix)

        self.setup_py('register', *args)

    def register_args(self, spec, prefix):
        """Arguments to pass to register."""
        return []

    def bdist(self, spec, prefix):
        """Create a built (binary) distribution."""
        args = self.bdist_args(spec, prefix)

        self.setup_py('bdist', *args)

    def bdist_args(self, spec, prefix):
        """Arguments to pass to bdist."""
        return []

    def bdist_dumb(self, spec, prefix):
        '''Create a "dumb" built distribution.'''
        args = self.bdist_dumb_args(spec, prefix)

        self.setup_py('bdist_dumb', *args)

    def bdist_dumb_args(self, spec, prefix):
        """Arguments to pass to bdist_dumb."""
        return []

    def bdist_rpm(self, spec, prefix):
        """Create an RPM distribution."""
        args = self.bdist_rpm(spec, prefix)

        self.setup_py('bdist_rpm', *args)

    def bdist_rpm_args(self, spec, prefix):
        """Arguments to pass to bdist_rpm."""
        return []

    def bdist_wininst(self, spec, prefix):
        """Create an executable installer for MS Windows."""
        args = self.bdist_wininst_args(spec, prefix)

        self.setup_py('bdist_wininst', *args)

    def bdist_wininst_args(self, spec, prefix):
        """Arguments to pass to bdist_wininst."""
        return []

    def upload(self, spec, prefix):
        """Upload binary package to PyPI."""
        args = self.upload_args(spec, prefix)

        self.setup_py('upload', *args)

    def upload_args(self, spec, prefix):
        """Arguments to pass to upload."""
        return []

    def check(self, spec, prefix):
        """Perform some checks on the package."""
        args = self.check_args(spec, prefix)

        self.setup_py('check', *args)

    def check_args(self, spec, prefix):
        """Arguments to pass to check."""
        return []
