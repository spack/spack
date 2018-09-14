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


class Sambamba(Package):
    """Sambamba: process your BAM data faster (bioinformatics)"""

    homepage = "http://lomereiter.github.io/sambamba/"
    git      = "https://github.com/lomereiter/sambamba.git"

    version('0.6.6', tag='v0.6.6', submodules=True)

    depends_on('ldc~shared', type=('build', 'link'))
    depends_on('python', type='build')

    resource(
        name='undeaD',
        git='https://github.com/dlang/undeaD.git',
        tag='v1.0.7',
    )

    patch('Makefile.patch')
    parallel = False

    def install(self, spec, prefix):
        make('sambamba-ldmd2-64')
        mkdirp(prefix.bin)
        for filename in ('build/sambamba', 'build/sambamba.debug'):
            install(filename, prefix.bin)
