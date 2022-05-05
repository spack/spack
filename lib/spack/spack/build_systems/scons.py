# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import inspect

import spack.builder
import spack.package
from spack.directives import buildsystem, depends_on

scons = spack.builder.BuilderMeta.make_decorator('scons')


class SConsPackage(spack.package.PackageBase):
    """Specialized class for packages built using SCons.

    See http://scons.org/documentation.html for more information.

    This class provides the following phases that can be overridden:

    1. :py:meth:`~.SConsBuilder.PackageWrapper.build`
    2. :py:meth:`~.SConsBuilder.PackageWrapper.install`

    Packages that use SCons as a build system are less uniform than packages
    that use other build systems. Developers can add custom subcommands or
    variables that control the build. You will likely need to override
    :py:meth:`~.SConsBuilder.PackageWrapper.build_args` to pass the appropriate variables.
    """
    #: To be used in UI queries that require to know which
    #: build-system class we are using
    build_system_class = 'SConsPackage'

    #: Callback names for build-time test
    build_time_test_callbacks = ['build_test']
    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = 'scons'

    buildsystem('scons')
    depends_on('scons', type='build', when='buildsystem=scons')


@spack.builder.builder('scons')
class SConsBuilder(spack.builder.Builder):
    #: Phases of a SCons package
    phases = ('build', 'install')

    class PackageWrapper(spack.builder.BuildWrapper):
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

        def build_test(self):
            """Run unit tests after build.

            By default, does nothing. Override this if you want to
            add package-specific tests.
            """
            pass

        scons.run_after('build')(
            spack.package.PackageBase._run_default_build_time_test_callbacks
        )

        # Check that self.prefix is there after installation
        scons.run_after('install')(spack.package.PackageBase.sanity_check_prefix)
