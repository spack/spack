##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class Meme(AutotoolsPackage):
    """The MEME Suite allows the biologist to discover novel motifs in
    collections of unaligned nucleotide or protein sequences, and to perform a
    wide variety of other motif-based analyses."""

    homepage = "http://meme-suite.org"
    url      = "http://meme-suite.org/meme-software/4.11.4/meme_4.11.4.tar.gz"

    version('4.11.4', '371f513f82fa0888205748e333003897')

    variant('mpi', default=True, description='Enable MPI support')

    depends_on('zlib', type=('link'))
    depends_on('libxml2', type=('link'))
    depends_on('libxslt', type=('link'))
    depends_on('libgcrypt', type=('link'))
    depends_on('perl', type=('build', 'run'))
    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('mpi', when='+mpi')

    # disable mpi support
    def configure_args(self):
        spec = self.spec
        args = []
        if '~mpi' in spec:
            args += ['--enable-serial']
        return args
