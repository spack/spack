# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


# Libiberty has two homes: binutils and gcc.  This package uses the
# binutils tarfile but only builds the libiberty subdirectory.  This
# is useful for other packages that want the demangling functions
# without the rest of binutils.

class Libiberty(AutotoolsPackage):
    """The libiberty.a library from GNU binutils.  Libiberty provides
    demangling and support functions for the GNU toolchain."""

    homepage = "https://www.gnu.org/software/binutils/"
    url      = "https://ftpmirror.gnu.org/binutils/binutils-2.31.1.tar.xz"

    version('2.31.1', '5b7c9d4ce96f507d95c1b9a255e52418')
    version('2.30',   'ffc476dd46c96f932875d1b2e27e929f')
    version('2.29.1', 'acc9cd826edb9954ac7cecb81c727793')
    version('2.28.1', 'a3bf359889e4b299fce1f4cb919dc7b6')

    variant('pic', default=False,
            description='Compile with position independent code.')

    # Configure and build just libiberty.
    configure_directory = 'libiberty'

    # Set default cflags (-g -O2), add -fPIC if requested, and move to
    # the configure line.
    def flag_handler(self, name, flags):
        if name != 'cflags':
            return (flags, None, None)

        if '-g' not in flags:
            flags.append('-g')

        for flag in flags:
            if flag.startswith('-O'):
                break
        else:
            flags.append('-O2')

        if '+pic' in self.spec:
            flags.append(self.compiler.pic_flag)

        return (None, None, flags)

    def configure_args(self):
        args = ['--enable-install-libiberty']
        return args
