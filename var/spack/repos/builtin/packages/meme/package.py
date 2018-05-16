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


class Meme(AutotoolsPackage):
    """The MEME Suite allows the biologist to discover novel motifs in
    collections of unaligned nucleotide or protein sequences, and to perform a
    wide variety of other motif-based analyses."""

    homepage = "http://meme-suite.org"
    url      = "http://meme-suite.org/meme-software/4.11.4/meme_4.11.4.tar.gz"

    version('4.12.0', '40d282cc33f7dedb06b24b9f34ac15c1')
    version('4.11.4', '371f513f82fa0888205748e333003897')

    variant('mpi', default=True, description='Enable MPI support')
    variant('image-magick', default=False, description='Enable image-magick for png output')

    depends_on('zlib', type=('link'))
    depends_on('libgcrypt', type=('link'))
    depends_on('perl', type=('build', 'run'))
    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('mpi', when='+mpi')
    depends_on('image-magick', type=('build', 'run'), when='+image-magick')
    depends_on('perl-xml-parser', type=('build', 'run'))

    def configure_args(self):
        spec = self.spec
        # have meme build its own versions of libxml2/libxslt, see #6736
        args = ['--enable-build-libxml2', '--enable-build-libxslt']
        if '~mpi' in spec:
            args += ['--enable-serial']
        return args
