# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Metabat(SConsPackage):
    """MetaBAT, an efficient tool for accurately reconstructing single
    genomes from complex microbial communities."""

    homepage = "https://bitbucket.org/berkeleylab/metabat"
    url      = "https://bitbucket.org/berkeleylab/metabat/get/v2.12.1.tar.gz"

    version('2.12.1', 'c032f47a8b24e58a5a9fefe52cb6e0f8')
    version('2.11.2', sha256='9baf81b385e503e71792706237c308a21ff9177a3211c79057dcecf8434e9a67')

    depends_on('boost@1.55.0:', type=('build', 'run'))
    depends_on('perl', type='run')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('BOOST_ROOT', self.spec['boost'].prefix)

    def install_args(self, spec, prefix):
        return ["PREFIX={0}".format(prefix)]

    @run_after('build')
    def fix_perl_scripts(self):
        filter_file(r'#!/usr/bin/perl',
                    '#!/usr/bin/env perl',
                    'aggregateBinDepths.pl')

        filter_file(r'#!/usr/bin/perl',
                    '#!/usr/bin/env perl',
                    'aggregateContigOverlapsByBin.pl')
