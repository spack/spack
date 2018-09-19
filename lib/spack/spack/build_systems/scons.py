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

import inspect

from spack.directives import depends_on
from spack.package import PackageBase, run_after


class SConsPackage(PackageBase):
    """Specialized class for packages built using SCons.

    See http://scons.org/documentation.html for more information.

    This class provides the following phases that can be overridden:

    1. :py:meth:`~.SConsPackage.build`
    2. :py:meth:`~.SConsPackage.install`

    Packages that use SCons as a build system are less uniform than packages
    that use other build systems. Developers can add custom subcommands or
    variables that control the build. You will likely need to override
    :py:meth:`~.SConsPackage.build_args` to pass the appropriate variables.
    """
    #: Phases of a SCons package
    phases = ['build', 'install']

    #: To be used in UI queries that require to know which
    #: build-system class we are using
    build_system_class = 'SConsPackage'

    #: Callback names for build-time test
    build_time_test_callbacks = ['test']

    depends_on('scons', type='build')

    def build_args(self, spec, prefix):
        """Arguments to pass to build."""
        return []

    def build(self, spec, prefix):
        """Build the package."""
        args = self.build_args(spec, prefix)

        inspect.getmodule(self).scons(*args)

    def install_args(self, spec, prefix):
        """Arguments to pass to install."""
        return []

    def install(self, spec, prefix):
        """Install the package."""
        args = self.install_args(spec, prefix)

        inspect.getmodule(self).scons('install', *args)

    # Testing

    def test(self):
        """Run unit tests after build.

        By default, does nothing. Override this if you want to
        add package-specific tests.
        """
        pass

    run_after('build')(PackageBase._run_default_build_time_test_callbacks)

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
