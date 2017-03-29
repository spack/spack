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
from spack.package import PackageBase, run_after, InstallError
from spack.util.executable import Executable


class PerlPackage(PackageBase):
    """Specialized class for packages that are built using Perl

    This class provides three phases that can be overridden:

        1. :py:meth:`~.PerlPackage.configure`
        2. :py:meth:`~.PerlPackage.build`
        3. :py:meth:`~.PerlPackage.install`

    They all have sensible defaults. Some packages may also need to override:

        +-----------------------------------------+--------------------------+
        | **Method**                              | **Purpose**              |
        +=========================================+==========================+
        | :py:attr:`~.PerlPackage.build_method    | Perl build method:       |
        |                                         | 'Makefile.PL' (default)  |
        |                                         | or 'Build.PL'            |
        +-----------------------------------------+--------------------------+
        | :py:meth:`~.PerlPackage.configure_args` | List of arguments for    |
        |                                         | Makefile.PL or Build.PL  |
        |                                         | (excluding prefix)       |
        +-----------------------------------------+--------------------------+
    """
    #: Phases of a Perl package
    phases = ['configure', 'build', 'install']

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'PerlPackage'

    #: This attribute is used to select the perl build method.
    #: Supported types are 'Makefile.PL' and 'Build.PL'.
    build_method = 'Makefile.PL'

    extends('perl')

    def configure_args(self):
        """Produces a list containing the arguments that must be passed to
        the configure method. The installation prefix is always prepended.

        :return: list of arguments for Makefile.PL or Build.PL
        """
        return []

    def configure(self, spec, prefix):
        """Runs Makefile.PL or Build.PL with the arguments specified in
        :py:meth:`.configure_args` and an appropriate installation prefix.
        """
        if self.build_method == 'Makefile.PL':
            options = ['Makefile.PL', 'INSTALL_BASE={0}'.format(prefix)]
        elif self.build_method == 'Build.PL':
            options = ['Build.PL', '--install_base', prefix]
        else:
            raise InstallError('Unknown build_method for perl package')
        options += self.configure_args()
        inspect.getmodule(self).perl(*options)

    def build(self, spec, prefix):
        """Builds a Perl package."""
        if self.build_method == 'Makefile.PL':
            makex = inspect.getmodule(self).make
            makex()
            if self.run_tests:
                makex('test')
        elif self.build_method == 'Build.PL':
            Buildx = Executable('./Build')
            Buildx()
            if self.run_tests:
                Buildx('test')
        else:
            raise InstallError('Unknown build_method for perl package')

    def install(self, spec, prefix):
        """Installs a Perl package."""
        if self.build_method == 'Makefile.PL':
            makex = inspect.getmodule(self).make
            makex('install')
        elif self.build_method == 'Build.PL':
            Buildx = Executable('./Build')
            Buildx('install')
        else:
            raise InstallError('Unknown build_method for perl package')

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
