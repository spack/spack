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

    version('0.170', '03599aee98c9b726c7a732a2dd0245d5')
    version('0.168', '52adfa40758d0d39e5d5c57689bf38d6')
    version('0.163', '77ce87f259987d2e54e4d87b86cbee41')

    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('gettext')
    conflicts('%gcc@7.2.0:', when='@0.163')

    provides('elf@1')

    # Elfutils uses nested functions in C code, which is implemented
    # in gcc, but not in clang. C code compiled with gcc is
    # binary-compatible with clang, so it should be possible to build
    # elfutils with gcc, and then link it to clang-built libraries.
    conflicts('%clang')

    def configure_args(self):
        # configure doesn't use LIBS correctly
        gettext_lib = self.spec['gettext'].prefix.lib,
        return [
            'LDFLAGS=-Wl,--no-as-needed -L%s -lintl' % gettext_lib,
            '--enable-maintainer-mode']
