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
