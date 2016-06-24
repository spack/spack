##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Glibc(Package):
    """Any Unix-like operating system needs a C library: the library which
    defines the ``system calls'' and other basic facilities such as open,
    malloc, printf, exit... The GNU C Library is used as the C library in the
    GNU system and in GNU/Linux systems, as well as many other systems that use
    Linux as the kernel."""

    homepage = "https://www.gnu.org/software/libc/"
    url = "http://open-source-box.org/glibc/glibc-2.23.tar.xz"

    version('2.23', '456995968f3acadbed39f5eba31678df')
    version('2.22', 'e51e02bf552a0a1fbbdc948fb2f5e83c')
    version('2.21', '9cb398828e8f84f57d1f7d5588cf40cd')
    version('2.20', '948a6e06419a01bd51e97206861595b0')
    version('2.19', 'e26b8cc666b162f999404b03970f14e4')
    version('2.18', '88fbbceafee809e82efd52efa1e3c58f')
    version('2.17', '87bf675c8ee523ebda4803e8e1cec638')
    version('2.16.0', '80b181b02ab249524ec92822c0174cf7')

    provides('libc')

    depends_on('binutils@2.20:')

    # Linux kernel headers 2.6.19 or later are required
    # depends_on("linux-headers")

    dynamic_linker = 'lib/ld-linux-x86-64.so.2'

    def install(self, spec, prefix):
        configure_args = [
            "--prefix={0}".format(prefix),
            "--disable-dependency-tracking",
            "--disable-debug",
            "--enable-obsolete=rpc",
            "--with-binutils={0}".format(spec['binutils'].prefix.bin)
        ]

        # Fix error: selinux/selinux.h: No such file or directory
        configure_args.append('--without-selinux')

        with working_dir("build", create=True):
            configure = Executable('../configure')
            configure(*configure_args)

            make()
            make('install')

        force_symlink('ld-linux-x86-64.so.2', join_path(prefix.lib, 'ld.so'))
