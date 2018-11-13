# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Redundans(Package):
    """Redundans pipeline assists an assembly of heterozygous genomes."""

    homepage = "https://github.com/Gabaldonlab/redundans"
    url      = "https://github.com/Gabaldonlab/redundans/archive/v0.13c.tar.gz"

    version('0.13c', '2003fb7c70521f5e430553686fd1a594')

    depends_on('python', type=('build', 'run'))
    depends_on('py-pyscaf', type=('build', 'run'))
    depends_on('py-fastaindex', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('perl', type=('build', 'run'))
    depends_on('sspace-standard')
    depends_on('bwa')
    depends_on('last')
    depends_on('gapcloser')
    depends_on('parallel')
    depends_on('snap-berkeley@1.0beta.18:', type=('build', 'run'))

    def install(self, spec, prefix):
        sspace_location = join_path(spec['sspace-standard'].prefix,
                                    'SSPACE_Standard_v3.0.pl')
        mkdirp(prefix.bin)
        filter_file(r'sspacebin = os.path.join(.*)$',
                    'sspacebin = \'' + sspace_location + '\'',
                    'redundans.py')
        install('redundans.py', prefix.bin)
        with working_dir('bin'):
            install('fasta2homozygous.py', prefix.bin)
            install('fasta2split.py', prefix.bin)
            install('fastq2insert_size.py', prefix.bin)
            install('fastq2mates.py', prefix.bin)
            install('fastq2shuffled.py', prefix.bin)
            install('fastq2sspace.py', prefix.bin)
            install('filterReads.py', prefix.bin)
