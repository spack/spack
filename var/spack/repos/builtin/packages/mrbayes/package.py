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
    url      = "https://github.com/NBISweden/MrBayes/releases/download/v3.2.7a/mrbayes-3.2.7a.tar.gz"

    version('3.2.7a', sha256='1a4670be84e6b968d59382328294db4c8ceb73e0c19c702265deec6f2177815c')
    version('3.2.7',  sha256='39d9eb269969b501268d5c27f77687c6eaa2c71ccf15c724e6f330fc405f24b9')

    variant('mpi', default=True, description='Enable MPI parallel support')
    variant('beagle', default=True, description='Enable BEAGLE library for speed benefits')
    variant('readline', default=True, description='Enable readline library')
    variant('sse', default=True, description='Enable SSE in order to substantially speed up execution')
    variant('avx', default=True, description='Enable AVX in order to substantially speed up execution')
    variant('fma', default=True, description='Enable FMA in order to substantially speed up execution')

    depends_on('libbeagle', when='+beagle')
    depends_on('mpi', when='+mpi')
    depends_on('readline', when='+readline')

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
