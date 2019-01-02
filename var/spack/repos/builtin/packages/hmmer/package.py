# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hmmer(Package):
    """HMMER is used for searching sequence databases for sequence homologs,
    and for making sequence alignments. It implements methods using
    probabilistic models called profile hidden Markov models (profile HMMs).
    """
    homepage = 'http://www.hmmer.org'
    url      = 'http://eddylab.org/software/hmmer/hmmer-3.2.1.tar.gz'

    version('3.2.1', '4e0ad5ed45462d4e36807d21e6d82b69')
    version('3.1b2', 'c8c141018bc0ccd7fc37b33f2b945d5f')
    version('3.0',   '4cf685f3bc524ba5b5cdaaa070a83588')
    version('2.4i',  'dab234c87e026ac1de942450750acd20')
    version('2.3.2', '5f073340c0cf761288f961a73821228a')
    version('2.3.1', 'c724413e5761c630892506698a4716e2')

    variant('mpi', default=True,  description='Compile with MPI')
    variant('gsl', default=False, description='Compile with GSL')

    depends_on('mpi', when='+mpi')
    depends_on('gsl', when='+gsl')

    def install(self, spec, prefix):
        configure_args = [
            '--prefix={0}'.format(prefix)
        ]

        if '+gsl' in self.spec:
            configure_args.extend([
                '--with-gsl',
                'LIBS=-lgsl -lgslcblas'
            ])

        if '+mpi' in self.spec:
            configure_args.append('--enable-mpi')

        configure(*configure_args)
        make()

        if self.run_tests:
            make('check')

        make('install')
