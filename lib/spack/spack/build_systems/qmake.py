# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


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
