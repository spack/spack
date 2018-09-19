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


class Redundans(Package):
    """Redundans pipeline assists an assembly of heterozygous genomes."""

    homepage = "https://github.com/Gabaldonlab/redundans"
    url      = "https://github.com/Gabaldonlab/redundans/archive/v0.13c.tar.gz"

    version('0.13c', '2003fb7c70521f5e430553686fd1a594')

    depends_on('python', type=('build', 'run'))
    depends_on('py-pyscaf', type=('build', 'run'))
    depends_on('py-fastaindex', type=('build', 'run'))
    depends_on('perl', type=('build', 'run'))
    depends_on('sspace-standard')
    depends_on('bwa')
    depends_on('last')
    depends_on('gapcloser')
    depends_on('parallel')
    depends_on('snap-berkeley')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('redundans.py', prefix.bin)
        with working_dir('bin'):
            install('fasta2homozygous.py', prefix.bin)
            install('fasta2split.py', prefix.bin)
            install('fastq2insert_size.py', prefix.bin)
            install('fastq2mates.py', prefix.bin)
            install('fastq2shuffled.py', prefix.bin)
            install('fastq2sspace.py', prefix.bin)
            install('filterReads.py', prefix.bin)
