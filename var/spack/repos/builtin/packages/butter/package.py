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


class Butter(Package):
    """butter: Bowtie UTilizing iTerative placEment of Repetitive small rnas.
       A wrapper for bowtie to produce small RNA-seq alignments where
       multimapped small RNAs tend to be placed near regions of confidently
       high density."""

    homepage = "https://github.com/MikeAxtell/butter"
    url      = "https://github.com/MikeAxtell/butter/archive/v0.3.3.tar.gz"

    version('0.3.3', '806ff3cb7afc1d8b75126404056c629d')

    depends_on('perl', type=('build', 'run'))
    depends_on('samtools')
    depends_on('bowtie')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('butter', prefix.bin)
        install('bam2wig', prefix.bin)
