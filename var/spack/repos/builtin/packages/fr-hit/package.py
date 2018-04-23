##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
