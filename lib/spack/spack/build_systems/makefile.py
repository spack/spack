# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import inspect
from typing import List  # novm

import llnl.util.tty as tty
from llnl.util.filesystem import working_dir

import spack.builder
import spack.package
from spack.directives import buildsystem, conflicts

# Decorator used to record callbacks and phases related to autotools
makefile = spack.builder.BuilderMeta.make_decorator('makefile')


class MakefilePackage(spack.package.PackageBase):
    """Specialized class for packages that are built using editable Makefiles

    This class provides three phases that can be overridden:

        1. :py:meth:`~.MakefilePackage.edit`
        2. :py:meth:`~.MakefilePackage.build`
        3. :py:meth:`~.MakefilePackage.install`

    It is usually necessary to override the :py:meth:`~.MakefilePackage.edit`
    phase, while :py:meth:`~.MakefilePackage.build` and
    :py:meth:`~.MakefilePackage.install` have sensible defaults.
    For a finer tuning you may override:

        +-----------------------------------------------+--------------------+
        | **Method**                                    | **Purpose**        |
        +===============================================+====================+
        | :py:attr:`~.MakefilePackage.build_targets`    | Specify ``make``   |
        |                                               | targets for the    |
        |                                               | build phase        |
        +-----------------------------------------------+--------------------+
        | :py:attr:`~.MakefilePackage.install_targets`  | Specify ``make``   |
        |                                               | targets for the    |
        |                                               | install phase      |
        +-----------------------------------------------+--------------------+
        | :py:meth:`~.MakefilePackage.build_directory`  | Directory where the|
        |                                               | Makefile is located|
        +-----------------------------------------------+--------------------+
    """
    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'MakefilePackage'
    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = 'makefile'

    buildsystem('makefile')
    conflicts('platform=windows')


class MakefileWrapper(spack.builder.BuildWrapper):
    #: Targets for ``make`` during the :py:meth:`~.MakefilePackage.build`
    #: phase
    build_targets = []  # type: List[str]
    #: Targets for ``make`` during the :py:meth:`~.MakefilePackage.install`
    #: phase
    install_targets = ['install']

    #: Callback names for build-time test
    build_time_test_callbacks = ['check']

    #: Callback names for install-time test
    install_time_test_callbacks = ['installcheck']

    @property
    def build_directory(self):
        """Returns the directory containing the main Makefile

        :return: build directory
        """
        return self.stage.source_path

    def edit(self, spec, prefix):
        """Edits the Makefile before calling make. This phase cannot
        be defaulted.
        """
        tty.msg('Using default implementation: skipping edit phase.')

    def build(self, spec, prefix):
        """Calls make, passing :py:attr:`~.MakefilePackage.build_targets`
        as targets.
        """
        with working_dir(self.build_directory):
            inspect.getmodule(self).make(*self.build_targets)

    def install(self, spec, prefix):
        """Calls make, passing :py:attr:`~.MakefilePackage.install_targets`
        as targets.
        """
        with working_dir(self.build_directory):
            inspect.getmodule(self).make(*self.install_targets)

    makefile.run_after('build')(
        spack.package.PackageBase._run_default_build_time_test_callbacks
    )

    def check(self):
        """Searches the Makefile for targets ``test`` and ``check``
        and runs them if found.
        """
        with working_dir(self.build_directory):
            self._if_make_target_execute('test')
            self._if_make_target_execute('check')

    makefile.run_after('install')(
        spack.package.PackageBase._run_default_install_time_test_callbacks
    )

    def installcheck(self):
        """Searches the Makefile for an ``installcheck`` target
        and runs it if found.
        """
        with working_dir(self.build_directory):
            self._if_make_target_execute('installcheck')

    # Check that self.prefix is there after installation
    makefile.run_after('install')(spack.package.PackageBase.sanity_check_prefix)

    # On macOS, force rpaths for shared library IDs and remove duplicate rpaths
    makefile.run_after('install')(spack.package.PackageBase.apply_macos_rpath_fixups)


@spack.builder.builder('makefile')
class MakefileBuilder(spack.builder.Builder):
    phases = ('edit', 'build', 'install')

    PackageWrapper = MakefileWrapper
