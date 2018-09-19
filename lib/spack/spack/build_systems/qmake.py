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


class QMakePackage(PackageBase):
    """Specialized class for packages built using qmake.

    For more information on the qmake build system, see:
    http://doc.qt.io/qt-5/qmake-manual.html

    This class provides three phases that can be overridden:

    1. :py:meth:`~.QMakePackage.qmake`
    2. :py:meth:`~.QMakePackage.build`
    3. :py:meth:`~.QMakePackage.install`

    They all have sensible defaults and for many packages the only thing
    necessary will be to override :py:meth:`~.QMakePackage.qmake_args`.
    """
    #: Phases of a qmake package
    phases = ['qmake', 'build', 'install']

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'QMakePackage'

    #: Callback names for build-time test
    build_time_test_callbacks = ['check']

    depends_on('qt', type='build')

    def qmake_args(self):
        """Produces a list containing all the arguments that must be passed to
        qmake
        """
        return []

    def qmake(self, spec, prefix):
        """Run ``qmake`` to configure the project and generate a Makefile."""
        inspect.getmodule(self).qmake(*self.qmake_args())

    def build(self, spec, prefix):
        """Make the build targets"""
        inspect.getmodule(self).make()

    def install(self, spec, prefix):
        """Make the install targets"""
        inspect.getmodule(self).make('install')

    # Tests

    def check(self):
        """Searches the Makefile for a ``check:`` target and runs it if found.
        """
        self._if_make_target_execute('check')

    run_after('build')(PackageBase._run_default_build_time_test_callbacks)

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
