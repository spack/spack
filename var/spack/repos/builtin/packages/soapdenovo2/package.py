# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Soapdenovo2(MakefilePackage):
    """SOAPdenovo is a novel short-read assembly method that can build a de
       novo draft assembly for the human-sized genomes. The program is
       specially designed to assemble Illumina GA short reads. It creates
       new opportunities for building reference sequences and carrying out
       accurate analyses of unexplored genomes in a cost effective way."""

    homepage = "https://github.com/aquaskyline/SOAPdenovo2"
    url      = "https://github.com/aquaskyline/SOAPdenovo2/archive/r240.tar.gz"

    version('240', '3bc6b63edf87bb47874bb6f126e43cd4')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('SOAPdenovo-63mer', prefix.bin)
        install('SOAPdenovo-127mer', prefix.bin)
