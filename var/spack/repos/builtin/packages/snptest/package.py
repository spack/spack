# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Snptest(Package):
    """SNPTEST is a program for the analysis of single SNP association in
       genome-wide studies."""

    homepage = "https://mathgen.stats.ox.ac.uk/genetics_software/snptest/snptest.html"
    url = "http://www.well.ox.ac.uk/~gav/resources/snptest_v2.5.2_linux_x86_64_dynamic.tgz"

    version('2.5.2', 'e3f2cc0351f260cf29369dc4f79a660a')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('snptest_v{0}'.format(self.version), prefix.bin)
