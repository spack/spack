# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Prank(Package):
    """A powerful multiple sequence alignment browser."""

    homepage = "http://wasabiapp.org/software/prank/"
    url      = "http://wasabiapp.org/download/prank/prank.source.150803.tgz"

    version('170427', sha256='623eb5e9b5cb0be1f49c3bf715e5fabceb1059b21168437264bdcd5c587a8859')

    depends_on('mafft')
    depends_on('exonerate')
    depends_on('bpp-suite')      # for bppancestor
    conflicts('%gcc@7.2.0', when='@:150803')

    def install(self, spec, prefix):
        with working_dir('src'):
            make()
            mkdirp(prefix.bin)
            install('prank', prefix.bin)
