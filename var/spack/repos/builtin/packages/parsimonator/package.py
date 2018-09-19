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


class Parsimonator(MakefilePackage):
    """Parsimonator is a no-frills light-weight implementation for building
       starting trees under parsimony for RAxML"""

    homepage = "http://www.exelixis-lab.org/"
    git      = "https://github.com/stamatak/Parsimonator-1.0.2.git"

    version('1.0.2', commit='78368c6ab1e9adc7e9c6ec9256dd7ff2a5bb1b0a')

    variant('sse', default=True, description='Enable SSE in order to substantially speed up execution')
    variant('avx', default=False, description='Enable AVX in order to substantially speed up execution')

    conflicts('+avx', when='+sse')

    @property
    def makefile_file(self):
        if '+sse' in self.spec:
            return 'Makefile.SSE3.gcc'
        elif '+avx' in self.spec:
            return 'Makefile.AVX.gcc'
        else:
            return 'Makefile.gcc'

    def edit(self, spec, prefix):
        makefile = FileFilter(self.makefile_file)
        makefile.filter('CC = gcc', 'CC = %s' % spack_cc)

    def build(self, spec, prefix):
        make('-f', self.makefile_file)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        if '+sse' in spec:
            install('parsimonator-SSE3', prefix.bin)
        elif '+avx' in spec:
            install('parsimonator-AVX', prefix.bin)
        else:
            install('parsimonator', prefix.bin)
