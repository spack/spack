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
from glob import glob


class Bowtie2(Package):
    """Bowtie 2 is an ultrafast and memory-efficient tool for aligning
       sequencing reads to long reference sequences"""

    homepage = "bowtie-bio.sourceforge.net/bowtie2/index.shtml"
    url      = "http://downloads.sourceforge.net/project/bowtie-bio/bowtie2/2.3.1/bowtie2-2.3.1-source.zip"

    version('2.3.1', 'b4efa22612e98e0c23de3d2c9f2f2478')
    version('2.2.5', '51fa97a862d248d7ee660efc1147c75f')

    depends_on('tbb', when='@2.3.1')
    depends_on('readline')
    depends_on('zlib')

    patch('bowtie2-2.2.5.patch', when='@2.2.5', level=0)
    patch('bowtie2-2.3.1.patch', when='@2.3.1', level=0)

    # seems to have trouble with 6's -std=gnu++14
    conflicts('%gcc@6:')

    def install(self, spec, prefix):
        make()
        mkdirp(prefix.bin)
        for bow in glob("bowtie2*"):
            install(bow, prefix.bin)
        # install('bowtie2',prefix.bin)
        # install('bowtie2-align-l',prefix.bin)
        # install('bowtie2-align-s',prefix.bin)
        # install('bowtie2-build',prefix.bin)
        # install('bowtie2-build-l',prefix.bin)
        # install('bowtie2-build-s',prefix.bin)
        # install('bowtie2-inspect',prefix.bin)
        # install('bowtie2-inspect-l',prefix.bin)
        # install('bowtie2-inspect-s',prefix.bin)
