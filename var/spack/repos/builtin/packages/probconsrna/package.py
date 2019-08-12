# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Probconsrna(Package):
    """Experimental version of PROBCONS with parameters estimated via
       unsupervised training on BRAliBASE """

    homepage = "http://probcons.stanford.edu/"
    url      = "http://probcons.stanford.edu/probconsRNA.tar.gz"

    version('2005-6-7', '2aa13012124208ca5dd6b0a1d508208d')

    def install(self, build, prefix):
        mkdirp(prefix.bin)
        install('compare', prefix.bin)
        install('makegnuplot', prefix.bin)
        install('probcons', prefix.bin)
        # needed for tcoffee
        install('probcons', prefix.bin.probconsRNA)
        install('project', prefix.bin)
