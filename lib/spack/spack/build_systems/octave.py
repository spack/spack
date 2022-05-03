# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import inspect

import spack.builder
from spack.directives import buildsystem, extends
from spack.multimethod import when
from spack.package import PackageBase, run_after

octave = spack.builder.BuilderMeta.make_decorator('octave')


class OctavePackage(PackageBase):
    """Specialized class for Octave packages. See
    https://www.gnu.org/software/octave/doc/v4.2.0/Installing-and-Removing-Packages.html
    for more information.

    This class provides the following phases that can be overridden:

    1. :py:meth:`~.OctavePackage.install`

    """
    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = 'OctavePackage'
    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = 'octave'

    buildsystem('octave')
    with when('buildsystem=octave'):
        extends('octave')


@spack.builder.builder('octave')
class OctaveBuilder(spack.builder.Builder):
    phases = ('install',)

    class PackageWrapper(spack.builder.BuildWrapper):
        def setup_build_environment(self, env):
            # octave does not like those environment variables to be set:
            env.unset('CC')
            env.unset('CXX')
            env.unset('FC')

        def install(self, spec, prefix):
            """Install the package from the archive file"""
            inspect.getmodule(self).octave(
                '--quiet',
                '--norc',
                '--built-in-docstrings-file=/dev/null',
                '--texi-macros-file=/dev/null',
                '--eval', 'pkg prefix %s; pkg install %s' %
                (prefix, self.stage.archive_file))

        # Check that self.prefix is there after installation
        run_after('install')(PackageBase.sanity_check_prefix)
