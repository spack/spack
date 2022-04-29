# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import glob
import inspect

import spack.builder
import spack.package
from spack.directives import extends

ruby = spack.builder.BuilderMeta.make_decorator('ruby')


class RubyPackage(spack.package.PackageBase):
    """Specialized class for building Ruby gems.

    This class provides two phases that can be overridden if required:

    #. :py:meth:`~.RubyPackage.build`
    #. :py:meth:`~.RubyPackage.install`
    """

    maintainers = ['Kerilk']

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'RubyPackage'

    build_system = 'ruby'

    extends('ruby')


@spack.builder.builder('ruby')
class RubyBuilder(spack.builder.Builder):
    phases = ('build', 'install')

    class PackageWrapper(spack.builder.BuildWrapper):
        def build(self, spec, prefix):
            """Build a Ruby gem."""

            # ruby-rake provides both rake.gemspec and Rakefile, but only
            # rake.gemspec can be built without an existing rake installation
            gemspecs = glob.glob('*.gemspec')
            rakefiles = glob.glob('Rakefile')
            if gemspecs:
                inspect.getmodule(self).gem('build', '--norc', gemspecs[0])
            elif rakefiles:
                jobs = inspect.getmodule(self).make_jobs
                inspect.getmodule(self).rake('package', '-j{0}'.format(jobs))
            else:
                # Some Ruby packages only ship `*.gem` files, so nothing to build
                pass

        def install(self, spec, prefix):
            """Install a Ruby gem.

            The ruby package sets ``GEM_HOME`` to tell gem where to install to."""

            gems = glob.glob('*.gem')
            if gems:
                # if --install-dir is not used, GEM_PATH is deleted from the
                # environement, and Gems required to build native extensions will
                # not be found. Those extensions are built during `gem install`.
                inspect.getmodule(self).gem(
                    'install', '--norc', '--ignore-dependencies',
                    '--install-dir', prefix, gems[0])

        # Check that self.prefix is there after installation
        ruby.run_after('install')(spack.package.PackageBase.sanity_check_prefix)
