# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Impute2(Package):
    """IMPUTE2 is a genotype imputation and haplotype phasing program based on
       ideas from Howie et al. 2009."""

    homepage = "https://mathgen.stats.ox.ac.uk/impute/impute_v2.html#home"
    url      = "https://mathgen.stats.ox.ac.uk/impute/impute_v2.3.2_x86_64_dynamic.tgz"

    version('2.3.2', '0e1bafb8f63eb5cf9ae02ab761af58aa')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('impute2', prefix.bin)
