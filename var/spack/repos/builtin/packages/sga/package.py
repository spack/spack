# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sga(AutotoolsPackage):
    """SGA is a de novo genome assembler based on the concept of string graphs.
       The major goal of SGA is to be very memory efficient, which is achieved
       by using a compressed representation of DNA sequence reads."""

    homepage = "https://www.msi.umn.edu/sw/sga"
    url      = "https://github.com/jts/sga/archive/v0.10.15.tar.gz"

    version('0.10.15', '990aed1593f8072650c6366e5cf32519')
    version('0.10.14', '211edb372898d6515dcde98d17078b7b')
    version('0.10.13', 'd4f6aefc48c940dba96cc6513649ecdd')
    version('0.10.12', '993bc165b4c77b75a5a2fe01c200c0da')
    version('0.10.11', 'b649da5471209f50df2d53f0f2bfa0ed')
    version('0.10.10', '494ff18d82b34cdaf8432b48b0356aae')
    version('0.10.9',  'c2111bfd278d8faaab19732aec79fa78')
    version('0.10.8',  '4d75f836eaae6018d993a0b75326014a')
    version('0.10.3',  'b12d35b24ca8a63c4dcc9f5d7e7c4133')

    depends_on('zlib')
    depends_on('sparsehash')
    depends_on('jemalloc')
    depends_on('bamtools')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    configure_directory = 'src'

    def configure_args(self):
        return [
            '--with-sparsehash={0}'.format(self.spec['sparsehash'].prefix),
            '--with-bamtools={0}'.format(self.spec['bamtools'].prefix),
            '--with-jemalloc={0}'.format(self.spec['jemalloc'].prefix)
        ]
