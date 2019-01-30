# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Csdp(MakefilePackage):
    """CSDP is a library of routines that implements a predictor corrector
       variant of the semidefinite programming algorithm of Helmberg, Rendl,
       Vanderbei, and Wolkowicz"""

    homepage = "https://projects.coin-or.org/Csdp"
    url      = "http://www.coin-or.org/download/source/Csdp/Csdp-6.1.1.tgz"

    version('6.1.1', '8388e8988e337bb5c1291068828de801')

    depends_on('atlas')

    def edit(self, spec, prefix):
        mkdirp(prefix.bin)
        makefile = FileFilter('Makefile')
        makefile.filter('/usr/local/bin', prefix.bin)
