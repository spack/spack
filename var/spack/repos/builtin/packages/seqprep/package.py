# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Seqprep(MakefilePackage):
    """SeqPrep is a program to merge paired end Illumina reads that are
       overlapping into a single longer read."""

    homepage = "https://github.com/jstjohn/SeqPrep"
    url      = "https://github.com/jstjohn/SeqPrep/archive/v1.3.2.tar.gz"

    version('1.3.2', 'b6a4f5491dfdb0ce38bf791454151468')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('SeqPrep', prefix.bin)
