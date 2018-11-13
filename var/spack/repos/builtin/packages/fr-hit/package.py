# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FrHit(Package):
    """An efficient algorithm for fragment recruitment for next generation
    sequences against microbial reference genomes."""

    homepage = "http://weizhong-lab.ucsd.edu/frhit"
    url      = "http://weizhong-lab.ucsd.edu/frhit/fr-hit-v0.7.1-2013-02-20.tar.gz"

    version('0.7.1-2013-02-20', '3e8ea41ba09ab0c13e9973fe6f493f96')

    depends_on('perl')
    depends_on('python@2.7:')

    # The patch adds the python interpreter to the beginning of the script
    # allowing it to be run directly without passing the entire path to the
    # script to python.
    patch('binning.patch')

    def install(self, spec, prefix):
        make()

        filter_file(
            r'#!/bin/env perl',
            '#!/usr/bin/env perl',
            'frhit2pairend.pl'
        )
        filter_file(
            r'#!/bin/env perl',
            '#!/usr/bin/env perl',
            'psl2sam.pl'
        )

        mkdirp(prefix.bin)
        install('fr-hit', prefix.bin)
        install('frhit2pairend.pl', prefix.bin)
        install('psl2sam.pl', prefix.bin)
        install('binning-1.1.1/bacteria_gitax.pkl', prefix.bin)
        install('binning-1.1.1/binning.py', prefix.bin)
        install('binning-1.1.1/tax.pkl', prefix.bin)
