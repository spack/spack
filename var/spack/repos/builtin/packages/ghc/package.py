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


class Ghc(AutotoolsPackage):
    """The Glasgow Haskell Compiler"""

    homepage = "https://www.haskell.org/ghc"
    url      = "https://downloads.haskell.org/~ghc/8.2.1/ghc-8.2.1-x86_64-deb7-linux.tar.xz"

    version('8.2.1', '4113498c83567ad32dd8d3dc4f64dc20')

    depends_on('perl', type=('build', 'run'))
    depends_on('python', type=('build', 'run'))
    depends_on('py-sphinx', type=('build', 'run'))
    depends_on('readline')
    depends_on('gmp')
    depends_on('ncurses')

    def url_for_version(self, version):
        url = 'https://downloads.haskell.org/~ghc/{0}/ghc-{0}-x86_64-deb7-linux.tar.xz'
        return url.format(version)

    def build(self, spec, prefix):
        # no make command, just make install which combines both
        pass
