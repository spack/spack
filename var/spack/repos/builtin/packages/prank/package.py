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


class Prank(Package):
    """A powerful multiple sequence alignment browser."""

    homepage = "http://wasabiapp.org/software/prank/"
    url      = "http://wasabiapp.org/download/prank/prank.source.150803.tgz"

    version('170427', 'a5cda14dc4e5efe1f14b84eb7a7caabd')
    version('150803', '71ac2659e91c385c96473712c0a23e8a')

    depends_on('mafft')
    depends_on('exonerate')
    depends_on('bpp-suite')      # for bppancestor
    conflicts('%gcc@7.2.0', when='@:150803')

    def install(self, spec, prefix):
        with working_dir('src'):
            make()
            mkdirp(prefix.bin)
            install('prank', prefix.bin)
