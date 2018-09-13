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


class Freebayes(MakefilePackage):
    """Bayesian haplotype-based genetic polymorphism discovery and
       genotyping."""

    homepage = "https://github.com/ekg/freebayes"
    git      = "https://github.com/ekg/freebayes.git"

    version('1.1.0', commit='39e5e4bcb801556141f2da36aba1df5c5c60701f',
            submodules=True)

    depends_on('cmake', type='build')
    depends_on('zlib')

    parallel = False

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        b = prefix.bin
        makefile.filter('cp bin/freebayes bin/bamleftalign /usr/local/bin/',
                        'cp bin/freebayes bin/bamleftalign {0}'.format(b))

    @run_before('install')
    def make_prefix_dot_bin(self):
        mkdir(prefix.bin)
