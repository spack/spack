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


class Elfutils(AutotoolsPackage):
    """elfutils is a collection of various binary tools such as
    eu-objdump, eu-readelf, and other utilities that allow you to
    inspect and manipulate ELF files. Refer to Table 5.Tools Included
    in elfutils for Red Hat Developer for a complete list of binary
    tools that are distributed with the Red Hat Developer Toolset
    version of elfutils."""

    homepage = "https://fedorahosted.org/elfutils/"

    url = "https://sourceware.org/elfutils/ftp/0.168/elfutils-0.168.tar.bz2"
    list_url = "https://sourceware.org/elfutils/ftp"
    list_depth = 1

    version('0.173', '35decb1ebfb90d565e4c411bee4185cc')
    version('0.170', '03599aee98c9b726c7a732a2dd0245d5')
    version('0.168', '52adfa40758d0d39e5d5c57689bf38d6')
    version('0.163', '77ce87f259987d2e54e4d87b86cbee41')

    # Libraries for reading compressed DWARF sections.
    variant('bzip2', default=False,
            description='Support bzip2 compressed sections.')
    variant('xz', default=False,
            description='Support xz compressed sections.')

    # Native language support from libintl.
    variant('nls', default=True,
            description='Enable Native Language Support.')

    depends_on('bzip2', type='link', when='+bzip2')
    depends_on('xz',    type='link', when='+xz')
    depends_on('zlib',  type='link')
    depends_on('gettext', when='+nls')

    conflicts('%gcc@7.2.0:', when='@0.163')

    provides('elf@1')

    # Elfutils uses nested functions in C code, which is implemented
    # in gcc, but not in clang. C code compiled with gcc is
    # binary-compatible with clang, so it should be possible to build
    # elfutils with gcc, and then link it to clang-built libraries.
    conflicts('%clang')

    def configure_args(self):
        spec = self.spec
        args = []

        if '+bzip2' in spec:
            args.append('--with-bzlib=%s' % spec['bzip2'].prefix)
        else:
            args.append('--without-bzlib')

        if '+xz' in spec:
            args.append('--with-lzma=%s' % spec['xz'].prefix)
        else:
            args.append('--without-lzma')

        # zlib is required
        args.append('--with-zlib=%s' % spec['zlib'].prefix)

        if '+nls' in spec:
            # configure doesn't use LIBS correctly
            args.append('LDFLAGS=-Wl,--no-as-needed -L%s -lintl' %
                        spec['gettext'].prefix.lib)
        else:
            args.append('--disable-nls')

        return args
