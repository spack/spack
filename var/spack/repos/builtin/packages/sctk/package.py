# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sctk(Package):
    """The NIST Scoring Toolkit (SCTK) is a collection of software tools
        designed to score benchmark test evaluations of Automatic Speech
        Recognition (ASR) Systems. The toolkit is currently used by NIST,
        benchmark test participants, and reserchers worldwide to as a
        common scoring engine."""

    homepage = "https://www.nist.gov/itl/iad/mig/tools"
    url      = "http://www.openslr.org/resources/4/sctk-2.4.10-20151007-1312Z.tar.bz2"

    version('2.4.10', 'dd01ad49a33486a4754655d06177f646',
            url='http://www.openslr.org/resources/4/sctk-2.4.10-20151007-1312Z.tar.bz2')
    version('2.4.9', '8cdab2a1263fe103481e23776e2178a1',
            url='http://www.openslr.org/resources/4/sctk-2.4.9-20141015-1634Z.tar.bz2')
    version('2.4.8', '2385209185b584e28dc42ea2cd324478',
            url='http://www.openslr.org/resources/4/sctk-2.4.8-20130429-2145.tar.bz2')
    version('2.4.0', '77912e75304098ffcc6850ecf641d1a4',
            url='http://www.openslr.org/resources/4/sctk-2.4.0-20091110-0958.tar.bz2')

    def install(self, spec, prefix):
        make('config')
        make('all')
        make('install')
        install_tree('bin', prefix.bin)
