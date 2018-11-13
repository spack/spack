# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Jags(AutotoolsPackage):
    """JAGS is Just Another Gibbs Sampler.  It is a program for analysis of
       Bayesian hierarchical models using Markov Chain Monte Carlo (MCMC)
       simulation not wholly unlike BUGS"""

    tags = ['mcmc', 'Gibbs sampler']

    homepage = "http://mcmc-jags.sourceforge.net/"
    url = "https://downloads.sourceforge.net/project/mcmc-jags/JAGS/4.x/Source/JAGS-4.2.0.tar.gz"

    version('4.3.0', 'd88dff326603deee39ce7fa4234c5a43')
    version('4.2.0', '9e521b3cfb23d3290a8c6bc0b79bf426')

    depends_on('blas')
    depends_on('lapack')

    def configure_args(self):
        args = ['--with-blas=%s' % self.spec['blas'].libs.ld_flags,
                '--with-lapack=%s' % self.spec['lapack'].libs.ld_flags]
        return args
