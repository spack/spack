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


class FastGbs(Package):
    """A bioinformatic pipeline designed to extract a high-quality SNP catalog
       starting from FASTQ files obtained from sequencing
       genotyping-by-sequencing (GBS) libraries."""

    homepage = "https://bitbucket.org/jerlar73/fast-gbs"
    git      = "https://bitbucket.org/jerlar73/fast-gbs.git"

    version('2017-01-25', commit='3b3cbffa84d269419692067c6a3de08b3b88849c')

    depends_on('parallel', type='run')
    depends_on('python@2.7:', type='run')
    depends_on('sabre', type='run')
    depends_on('py-cutadapt', type='run')
    depends_on('bwa', type='run')
    depends_on('samtools', type='run')
    depends_on('platypus', type='run')
    depends_on('py-pyvcf', type='run')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('fastgbs.sh', prefix.bin)
        install('parameters.txt', prefix.bin)
        install('makeDir.sh', prefix.bin)
        install('makeBarcodeSabre.py', prefix.bin)
        install('vcf2txt.py', prefix.bin)
        install('txt2unix.sh', prefix.bin)
