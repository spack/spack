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
from spack import *
import os.path
import shutil

# Libiberty has two homes: binutils and gcc.  This package uses the
# binutils tarfile but only builds the libiberty subdirectory.  This
# is useful for other packages that want the demangling functions
# without the rest of binutils.


class Libiberty(AutotoolsPackage):
    """The libiberty.a library from GNU binutils.  Libiberty provides
    demangling and support functions for the GNU toolchain."""

    homepage = "https://www.gnu.org/software/binutils/"
    url = "https://ftp.gnu.org/gnu/binutils/binutils-2.31.1.tar.xz"

    version('2.31.1', '5b7c9d4ce96f507d95c1b9a255e52418')
    version('2.30',   'ffc476dd46c96f932875d1b2e27e929f')
    version('2.29.1', 'acc9cd826edb9954ac7cecb81c727793')
    version('2.28.1', 'a3bf359889e4b299fce1f4cb919dc7b6')

    variant('fpic', default=False, description='Compile with -fPIC.')

    # Configure and build just libiberty.
    @property
    def configure_directory(self):
        return join_path(self.stage.source_path, 'libiberty')

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

        if '+fpic' in self.spec:
            flags.append(self.compiler.pic_flag)

        return (None, None, flags)

    def configure_args(self):
        args = ['--enable-install-libiberty']
        return args

    # Libiberty always installs libiberty.a into lib64, even with
    # --libdir or --disable-multilib, so just give up and copy.
    @run_after('install')
    def copy_library(self):
        lib_file = join_path(self.prefix.lib, 'libiberty.a')
        lib64_file = join_path(self.prefix.lib64, 'libiberty.a')

        if not os.path.isfile(lib_file):
            mkdirp(self.prefix.lib)
            shutil.copy(lib64_file, lib_file)
