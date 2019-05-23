# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from glob import glob


class PerlStarFusion(Package):
    """STAR-Fusion is a component of the Trinity Cancer Transcriptome Analysis
    Toolkit (CTAT). STAR-Fusion uses the STAR aligner to identify candidate
    fusion transcripts supported by Illumina reads. STAR-Fusion further
    processes the output generated by the STAR aligner to map junction reads
    and spanning reads to a reference annotation set."""

    homepage = "https://github.com/STAR-Fusion/STAR-Fusion"
    git      = "https://github.com/STAR-Fusion/STAR-Fusion.git"

    version('master', commit='8c5a541')

    extends('perl')

    depends_on('star', type=('build', 'run'))
    depends_on('perl', type=('build', 'run'))
    depends_on('perl-intervaltree', type=('build', 'run'))
    depends_on('perl-dbi', type=('build', 'run'))
    depends_on('perl-dbfile', type=('build', 'run'))
    depends_on('perl-uri-escape', type=('build', 'run'))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('STAR-Fusion', prefix.bin)
        mkdirp(perl_lib_dir)
        with working_dir('PerlLib'):
            for pm in glob("*.pm"):
                install(pm, perl_lib_dir)
        with working_dir('util'):
            for files in glob("*"):
                install(files, prefix.bin)
