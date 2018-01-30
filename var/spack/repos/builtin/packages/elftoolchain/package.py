##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Elftoolchain(Package):
    """ELF Tool Chain: a BSD-licensed implementation of tools for the ELF format

       ELF Tool Chain is A BSD-licensed implementation of compilation
       tools (nm, ar, as, ld, etc.) for the ELF object format."""

    homepage = "https://sourceforge.net/p/elftoolchain/wiki/Home/"
    url      = "https://sourceforge.net/projects/elftoolchain/files/Sources/elftoolchain-0.7.1/elftoolchain-0.7.1.tar.bz2"

    version('0.7.1', '47fe4cedded2edeaf8e429f1f842e23d')

    # Package won't link to libdwarf; does this provide enough of the ELF API for tools in spack?
    # provides('elf@0')

    depends_on('bmake', type='build')
    depends_on('bison', type='build')
    depends_on('flex', type='build')
    depends_on('libarchive')

    # Patches adapted from
    # https://github.com/macports/macports-ports/blob/master/devel/elftoolchain/files/patch-byteorder-macros.diff
    # https://github.com/macports/macports-ports/blob/master/devel/elftoolchain/files/patch-mk.diff
    patch('patch-byteorder-macros.patch', level=0)
    patch('patch-mk.patch', level=0)

    # Patches to avoid installing files as root user, wheel group; the
    # flags in the install phase below to disable installing files as
    # root user must be applied _in addition_ to these
    # patches. Patches are necessary because undefining BINOWN,
    # BINGRP, DOCOWN, and DOCGRP is insufficient -- it leads to syntax
    # errors thrown when `install` is called within the makefile.
    patch('mk-elftoolchain-inc-mk.patch', level=0)
    patch('mk-elftoolchain-lib-mk.patch', level=0)
    patch('mk-elftoolchain-tex-mk.patch', level=0)

    def install(self, spec, prefix):
        bmake = which('bmake')
        mkdirp(self.spec.prefix.bin)
        mkdirp(self.spec.prefix.lib)
        mkdirp(self.spec.prefix.include)
        mkdirp(self.spec.prefix.share.man)

        # Build phase; flags guessed from MacPorts
        # https://github.com/macports/macports-ports/blob/master/devel/elftoolchain/Portfile
        # 'prefix={0}'.format(self.spec.prefix),
        args = ['BINDIR=/bin',
                'LIBDIR=/lib',
                'SHLIBDIR=/lib',
                'INCSDIR=/include',
                'MANDIR=/{0}'.format(join_path('share', 'man')),
                'MANTARGET=man',
                'LIBARCHIVE_PREFIX={0}'.format(spec['libarchive'].prefix),
                'DESTDIR={0}'.format(prefix)]

        # Exclude tests (large build targets) and docs
        build_args = args
        build_args.append('WITH_TESTS=no')
        build_args.append('MKTEX=no')
        bmake(*build_args)

        # Install phase
        install_args = ['install'] + args

        # Do not strip binaries because it leads to errors
        install_args.append('STRIP=')

        # BSD make has a bunch of default privileges used as arguments
        # to `install` in '.mk' files in the directory encoded by
        # `spec['bmake'].prefix.share.mk`. These variables store user
        # and group flags to install headers, libraries, etc as the
        # root user. Undefining these flags eliminates permissions
        # errors during the install phase.
        install_args.append('LIB_INSTALL_OWN=')
        install_args.append('INC_INSTALL_OWN=')
        install_args.append('MAN_INSTALL_OWN=')
        install_args.append('BIN_INSTALL_OWN=')
        install_args.append('DOC_INSTALL_OWN=')
        install_args.append('FILES_INSTALL_OWN=')
        install_args.append('PROG_INSTALL_OWN=')

        bmake(*install_args)
