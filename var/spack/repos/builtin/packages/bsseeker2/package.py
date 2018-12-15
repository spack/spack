# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bsseeker2(Package):
    """A versatile aligning pipeline for bisulfite sequencing data."""

    homepage = "http://pellegrini.mcdb.ucla.edu/BS_Seeker2"
    url      = "https://github.com/BSSeeker/BSseeker2/archive/v2.1.2.tar.gz"

    version('2.1.2',     '5f7f0ef4071711e56b59c5c16b7f34a7')

    depends_on('python@2.6:2.999', type=('build', 'run'))
    depends_on('py-pysam', type=('build', 'run'))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('Antisense.py', prefix.bin)
        install_tree('bs_index', prefix.bin.bs_index)
        install('bs_seeker2-build.py', prefix.bin)
        install_tree('bs_utils', prefix.bin.bs_utils)
        install_tree('galaxy', prefix.bin.galaxy)
        install_tree('bs_align', prefix.bin.bs_align)
        install('bs_seeker2-align.py', prefix.bin)
        install('bs_seeker2-call_methylation.py', prefix.bin)
        install('FilterReads.py', prefix.bin)
