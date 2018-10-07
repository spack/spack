# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Price(MakefilePackage):
    """PRICE (Paired-Read Iterative Contig Extension): a de novo genome
       assembler implemented in C++."""

    homepage = "http://derisilab.ucsf.edu/software/price/"
    url      = "http://derisilab.ucsf.edu/software/price/PriceSource140408.tar.gz"

    version('140408', '2880274a514c34b812718b13a620813e')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('PriceTI', prefix.bin)
        install('PriceSeqFilter', prefix.bin)
