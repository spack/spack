# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tmalign(Package):
    """TM-align is an algorithm for sequence-order independent protein
       structure comparisons."""

    homepage = "http://zhanglab.ccmb.med.umich.edu/TM-align"
    url      = "http://zhanglab.ccmb.med.umich.edu/TM-align/TM-align-C/TMalignc.tar.gz"

    version('2016-05-25', 'c1027e4b65c07d1c5df9717de7417118')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('TMalign', prefix.bin)
