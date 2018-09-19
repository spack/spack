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


class Bracken(Package):
    """Bracken (Bayesian Reestimation of Abundance with KrakEN) is a highly
    accurate statistical method that computes the abundance of species in DNA
    sequences from a metagenomics sample."""

    homepage = "https://ccb.jhu.edu/software/bracken"
    url      = "https://github.com/jenniferlu717/Bracken/archive/1.0.0.tar.gz"

    version('1.0.0', 'bd91805655269c5f3becb8f8028bab6d')

    depends_on('perl')
    depends_on('python@2.7:')
    depends_on('perl-exporter-tiny')
    depends_on('perl-list-moreutils')
    depends_on('perl-parallel-forkmanager')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install_tree('sample_data', prefix.sample_data)

        filter_file(
            r'#!/bin/env perl',
            '#!/usr/bin/env perl',
            'count-kmer-abundances.pl'
        )

        filter_file(
            r'#!/usr/bin/python',
            '#!/usr/bin/env python',
            'est_abundance.py'
        )

        filter_file(
            r'#!/usr/bin/python',
            '#!/usr/bin/env python',
            'generate_kmer_distribution.py'
        )

        files = (
            'count-kmer-abundances.pl',
            'est_abundance.py',
            'generate_kmer_distribution.py',
        )

        chmod = which('chmod')
        for name in files:
            install(name, prefix.bin)
            chmod('+x', join_path(self.prefix.bin, name))
