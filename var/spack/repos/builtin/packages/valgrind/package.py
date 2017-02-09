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
import sys


class Valgrind(AutotoolsPackage):
    """An instrumentation framework for building dynamic analysis.

    There are Valgrind tools that can automatically detect many memory
    management and threading bugs, and profile your programs in
    detail. You can also use Valgrind to build new tools.

    Valgrind is Open Source / Free Software, and is freely available
    under the GNU General Public License, version 2.

    """
    homepage = "http://valgrind.org/"
    url = "http://valgrind.org/downloads/valgrind-3.11.0.tar.bz2"

    version('3.12.0', '6eb03c0c10ea917013a7622e483d61bb')
    version('3.11.0', '4ea62074da73ae82e0162d6550d3f129')
    version('3.10.1', '60ddae962bc79e7c95cfc4667245707f')
    version('3.10.0', '7c311a72a20388aceced1aa5573ce970')
    version('develop', svn='svn://svn.valgrind.org/valgrind/trunk')

    variant('mpi', default=True,
            description='Activates MPI support for valgrind')
    variant('boost', default=True,
            description='Activates boost support for valgrind')

    depends_on('mpi', when='+mpi')
    depends_on('boost', when='+boost')

    depends_on("autoconf", type='build', when='@develop')
    depends_on("automake", type='build', when='@develop')
    depends_on("libtool", type='build', when='@develop')

    def configure_args(self):
        spec = self.spec
        options = []
        if not (spec.satisfies('%clang') and sys.platform == 'darwin'):
            # Otherwise with (Apple's) clang there is a linker error:
            # clang: error: unknown argument: '-static-libubsan'
            options.append('--enable-ubsan')

        if sys.platform == 'darwin':
            options.extend([
                '--build=amd64-darwin',
                '--enable-only64bit'
            ])
        return options
