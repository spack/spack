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


class Blis(Package):
    """BLAS-like Library Instantiation Software Framework."""

    homepage = "https://github.com/flame/blis"
    url      = "https://github.com/flame/blis/archive/0.4.0.tar.gz"

    version('0.4.0', sha256='9c7efd75365a833614c01b5adfba93210f869d92e7649e0b5d9edc93fc20ea76')
    version('0.3.2', sha256='b87e42c73a06107d647a890cbf12855925777dc7124b0c7698b90c5effa7f58f')
    version('0.3.1', sha256='957f28d47c5cf71ffc62ce8cc1277e17e44d305b1c2fa8506b0b55617a9f28e4')
    version('0.3.0', sha256='d34d17df7bdc2be8771fe0b7f867109fd10437ac91e2a29000a4a23164c7f0da')
    version('0.2.2', sha256='4a7ecb56034fb20e9d1d8b16e2ef587abbc3d30cb728e70629ca7e795a7998e8')

    # TODO: Add configure variants.

    variant(
        'threads', default='none',
        description='Multithreading support',
        values=('pthreads', 'openmp', 'none'),
        multi=False
    )

    # virtual dependency
    provides('blas')
    provides('lapack')
 
    def configure_args(self, spec, prefix):
        config_args=[]
        # Add support for multithreading
        if self.spec.satisfies('threads=openmp'):
            config_args.append('--enable-threading[=openmp]')
        elif self.spec.satisfies('threads=pthreads'):
            config_args.append('--enable-threading[=pthreads]')
        else:
            config_args.append('--enable-threading[=no]')
        return config_args
    
    def install(self, spec, prefix):
        config_args = configure_args(self,spec,prefix)
        configure('auto',*config_args)
        make()
        make('install')
        make('check')
