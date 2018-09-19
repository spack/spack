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


class Mrbayes(AutotoolsPackage):
    """MrBayes is a program for Bayesian inference and model choice across a
       wide range of phylogenetic and evolutionary models. MrBayes uses Markov
       chain Monte Carlo (MCMC) methods to estimate the posterior distribution
       of model parameters."""

    homepage = "http://mrbayes.sourceforge.net"
    git      = "https://github.com/NBISweden/MrBayes.git"

    version('2017-11-22', commit='8a9adb11bcc538cb95d91d57568dff383f924503')

    variant('mpi', default=True, description='Enable MPI parallel support')
    variant('beagle', default=True, description='Enable BEAGLE library for speed benefits')
    variant('sse', default=True, description='Enable SSE in order to substantially speed up execution')

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
        if '~sse' in self.spec:
            args.append('--enable-sse=no')
        else:
            args.append('--enable-sse=yes')
        if '~mpi' in self.spec:
            args.append('--enable-mpi=no')
        else:
            args.append('--enable-mpi=yes')
        return args

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir('src'):
            install('mb', prefix.bin)
