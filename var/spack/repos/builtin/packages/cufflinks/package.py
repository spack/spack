# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cufflinks(Package):
    """Cufflinks assembles transcripts, estimates their abundances, and tests
       for differential expression and regulation in RNA-Seq samples."""

    homepage = "http://cole-trapnell-lab.github.io/cufflinks"
    url      = "http://cole-trapnell-lab.github.io/cufflinks/assets/downloads/cufflinks-2.2.1.Linux_x86_64.tar.gz"

    version('2.2.1', '7e693d182dcfda8aeef8523219ea9ea7')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('cuffcompare', prefix.bin)
        install('cuffdiff', prefix.bin)
        install('cufflinks', prefix.bin)
        install('cuffmerge', prefix.bin)
        install('cuffnorm', prefix.bin)
        install('cuffquant', prefix.bin)
        install('gffread', prefix.bin)
        install('gtf_to_sam', prefix.bin)
