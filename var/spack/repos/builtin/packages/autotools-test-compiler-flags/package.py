# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install autotools-test-compiler-flags
#
# You can edit this file again by typing:
#
#     spack edit autotools-test-compiler-flags
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import llnl.util.tty as tty


class AutotoolsTestCompilerFlags(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "https://github.com/LLNL/mpileaks/releases/download/v1.0/mpileaks-1.0.tar.gz"

    version('1.0', sha256='2e34cc4505556d1c1f085758e26f2f8eea0972db9382f051b2dcfb1d7d9e1825')

    # notify when the package is updated.
    maintainers = ['jjellio']

    variant('set_in_build_env',
            default='Undefined',
            multi=False,
            description='Pipe (|) separated lists of VAR=VAL you wish set in'
                        ' setup_build_environment-'
                        " Pipe because single valued variants won't allow"
                        " commas, semicolons, or spaces")

    variant('set_in_configure_args',
            default='Undefined',
            multi=False,
            description='Pipe (|) separated lists of VAR=VAL you wish set in'
                        ' configure_args -'
                        " Pipe because single valued variants won't allow"
                        " commas, semicolons, or spaces")

    # FIXME: Add dependencies if required.
    depends_on('mpi')

    def configure_args(self):
        spec = self.spec
        args = []

        args_to_set = spec.variants['set_in_configure_args'].value
        if args_to_set == 'Undefined':
            return args

        # do whatever was passed in
        args = [var_val for var_val in args_to_set.split('|')]
        for name, _, val in [arg.partition('=') for arg in args]:
            tty.msg('[configure_args] Setting {0}={1}'.format(name, val))
        return args

    def setup_build_environment(self, spack_env):
        spec = self.spec

        args_to_set = spec.variants['set_in_build_env'].value
        if args_to_set == 'Undefined':
            return

        # do whatever was passed in
        for name, _, val in [var_val.partition('=')
                             for var_val in args_to_set.split('|')]:
            spack_env.set(name, val)
            tty.msg('[setup_build_environment] Setting {0}={1}'.format(name, val))
