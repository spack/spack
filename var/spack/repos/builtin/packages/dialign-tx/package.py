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


class DialignTx(MakefilePackage):
    """DIALIGN-TX: greedy and progressive approaches for segment-based
       multiple sequence alignment"""

    homepage = "http://dialign-tx.gobics.de/"
    url      = "http://dialign-tx.gobics.de/DIALIGN-TX_1.0.2.tar.gz"

    version('1.0.2', '8ccfb1d91136157324d1e513f184ca29')

    build_directory = 'source'

    conflicts('%gcc@6:')

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            makefile = FileFilter('Makefile')
            makefile.filter(' -march=i686 ', ' ')
            makefile.filter('CC=gcc', 'CC=%s' % spack_cc)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.build_directory):
            install('dialign-tx', prefix.bin)
            # t-coffee recognizes as dialign-t
            install('dialign-tx', join_path(prefix.bin, 'dialign-t'))

    patch('dialign-1-0-2-gcc-5-4-0.patch', when='%gcc@5.4.0')
