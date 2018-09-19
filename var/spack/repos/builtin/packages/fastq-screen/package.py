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


class FastqScreen(Package):
    """FastQ Screen allows you to screen a library of sequences in FastQ format
       against a set of sequence databases so you can see if the composition of
       the library matches with what you expect."""

    homepage = "https://www.bioinformatics.babraham.ac.uk/projects/fastq_screen/"
    url      = "https://www.bioinformatics.babraham.ac.uk/projects/fastq_screen/fastq_screen_v0.11.2.tar.gz"

    version('0.11.2', 'ef79f16ee553aaa0ab2fc14ea11e5473')

    depends_on('perl', type='run')
    depends_on('perl-gd-graph', type='run')
    depends_on('bowtie')
    depends_on('bowtie2')
    depends_on('bwa')
    depends_on('samtools')

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)
