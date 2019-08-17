# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fastphase(Package):
    """Software for haplotype reconstruction, and estimating missing genotypes
       from population data."""

    homepage = "http://stephenslab.uchicago.edu/software.html"
    url      = "http://scheet.org/code/Linuxfp.tar.gz"

    version('2016-03-30', 'b48731eed9b8d0a5a321f970c5c20d8c')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('fastPHASE', prefix.bin)
