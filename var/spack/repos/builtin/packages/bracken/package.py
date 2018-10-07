# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
