# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hisea(MakefilePackage):
    """HISEA is an efficient all-vs-all long read aligner for SMRT sequencing
       data. Its algorithm is designed to produce highest alignment sensitivity
       among others."""

    homepage = "https://doi.org/10.1186/s12859-017-1953-9"
    url      = "https://github.com/lucian-ilie/HISEA"

    version('2017.12.26', '54211bdc33b7ce52a8f1e76845935eb8',
            url='https://github.com/lucian-ilie/HISEA/tarball/39e01e98caa0f2101da806ca59306296effe789c')

    depends_on('boost')

    def patch(self):
        if self.spec.target.family == 'aarch64':
            filter_file('-mpopcnt', '', 'Makefile')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('hisea', prefix.bin)
