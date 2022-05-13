# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import inspect

from llnl.util.filesystem import working_dir

import spack.builder
import spack.package
from spack.directives import buildsystem, depends_on

qmakebuild = spack.builder.BuilderMeta.make_decorator('qmake')


class QMakePackage(spack.package.PackageBase):
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
    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'QMakePackage'

    buildsystem('qmake')
    depends_on('qt', type='build', when='buildsystem=qmake')


@spack.builder.builder('qmake')
class QMakeBuilder(spack.builder.Builder):
    phases = ('qmake', 'build', 'install')

    class QMakeWrapper(spack.builder.BuildWrapper):
        #: Callback names for build-time test
        build_time_test_callbacks = ['check']

        @property
        def build_directory(self):
            """The directory containing the ``*.pro`` file."""
            return self.stage.source_path

        def qmake_args(self):
            """Produces a list containing all the arguments that must be passed to
            qmake
            """
            return []

        def qmake(self, spec, prefix):
            """Run ``qmake`` to configure the project and generate a Makefile."""

            with working_dir(self.build_directory):
                inspect.getmodule(self).qmake(*self.qmake_args())

        def build(self, spec, prefix):
            """Make the build targets"""

            with working_dir(self.build_directory):
                inspect.getmodule(self).make()

        def install(self, spec, prefix):
            """Make the install targets"""

            with working_dir(self.build_directory):
                inspect.getmodule(self).make('install')

        def check(self):
            """Searches the Makefile for a ``check:`` target and runs it if found.
            """

            with working_dir(self.build_directory):
                self._if_make_target_execute('check')

        qmakebuild.run_after('build')(
            spack.package.PackageBase._run_default_build_time_test_callbacks
        )
        # Check that self.prefix is there after installation
        qmakebuild.run_after('install')(spack.package.PackageBase.sanity_check_prefix)
