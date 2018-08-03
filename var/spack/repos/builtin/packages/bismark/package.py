##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Bismark(Package):
    """A tool to map bisulfite converted sequence reads and determine cytosine
    methylation states"""

    homepage = "https://www.bioinformatics.babraham.ac.uk/projects/bismark"
    url      = "https://github.com/FelixKrueger/Bismark/archive/0.19.0.tar.gz"

    version('0.19.0', 'f403654aded77bf0d1dac1203867ded1')
    version('0.18.2', '42334b7e3ed53ba246f30f1f846b4af8')

    depends_on('bowtie2', type='run')
    depends_on('perl', type='run')
    depends_on('samtools', type='run')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('bam2nuc', prefix.bin)
        install('bismark', prefix.bin)
        install('bismark_genome_preparation', prefix.bin)
        install('bismark_methylation_extractor', prefix.bin)
        install('bismark2bedGraph', prefix.bin)
        install('bismark2report', prefix.bin)
        install('bismark2summary', prefix.bin)
        install('coverage2cytosine', prefix.bin)
        install('deduplicate_bismark', prefix.bin)
        install('filter_non_conversion', prefix.bin)
        install('NOMe_filtering', prefix.bin)
