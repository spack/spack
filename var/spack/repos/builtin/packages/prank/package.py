# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Prank(Package):
    """A powerful multiple sequence alignment browser."""

    homepage = "http://wasabiapp.org/software/prank/"
    url      = "http://wasabiapp.org/download/prank/prank.source.150803.tgz"

    version('170427', 'a5cda14dc4e5efe1f14b84eb7a7caabd')
    version('150803', '71ac2659e91c385c96473712c0a23e8a')

    depends_on('mafft')
    depends_on('exonerate')
    depends_on('bpp-suite')      # for bppancestor
    conflicts('%gcc@7.2.0', when='@:150803')

    def install(self, spec, prefix):
        with working_dir('src'):
            make()
            mkdirp(prefix.bin)
            install('prank', prefix.bin)
