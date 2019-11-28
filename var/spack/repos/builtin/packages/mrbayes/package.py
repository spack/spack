# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mrbayes(AutotoolsPackage):
    """MrBayes is a program for Bayesian inference and model choice across a
       wide range of phylogenetic and evolutionary models. MrBayes uses Markov
       chain Monte Carlo (MCMC) methods to estimate the posterior distribution
       of model parameters."""

    homepage = "http://mrbayes.sourceforge.net"
    git      = "https://github.com/NBISweden/MrBayes.git"

    version('3.2.7a', commit='0176ac2d0bfed53a5bc0aaf3f5a3def71f23575f')

    variant('mpi', default=True, description='Enable MPI parallel support')
    variant('beagle', default=True, description='Enable BEAGLE library for speed benefits')
    variant('readline', default=True, description='Enable readline library')
    variant('sse', default=True, description='Enable SSE in order to substantially speed up execution')
    variant('avx', default=True, description='Enable AVX in order to substantially speed up execution')
    variant('fma', default=True, description='Enable FMA in order to substantially speed up execution')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('libbeagle', when='+beagle')
    depends_on('mpi', when='+mpi')

    def configure_args(self):
        args = []
        if '~beagle' in self.spec:
            args.append('--with-beagle=no')
        else:
            args.append('--with-beagle=%s' % self.spec['libbeagle'].prefix)
        if '~readline' in self.spec:
            args.append('--with-readline=no')
        else:
            args.append('--with-readline=yes')
        if '~sse' in self.spec:
            args.append('--enable-sse=no')
        else:
            args.append('--enable-sse=yes')
        if '~avx' in self.spec:
            args.append('--enable-avx=no')
        else:
            args.append('--enable-avx=yes')
        if '~fma' in self.spec:
            args.append('--enable-fma=no')
        else:
            args.append('--enable-fma=yes')
        if '~mpi' in self.spec:
            args.append('--with-mpi=no')
        else:
            args.append('--with-mpi=yes')
        return args

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir('src'):
            install('mb', prefix.bin)
