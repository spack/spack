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
import sys


class OsuMicroBenchmarks(AutotoolsPackage):
    """The Ohio MicroBenchmark suite is a collection of independent MPI
    message passing performance microbenchmarks developed and written at
    The Ohio State University. It includes traditional benchmarks and
    performance measures such as latency, bandwidth and host overhead
    and can be used for both traditional and GPU-enhanced nodes."""

    homepage = "http://mvapich.cse.ohio-state.edu/benchmarks/"
    url      = "http://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-5.3.tar.gz"

    version('5.4', '7e7551879b944d71b7cc60d476d5403b')
    version('5.3', '42e22b931d451e8bec31a7424e4adfc2')

    variant('cuda', default=False, description="Enable CUDA support")

    depends_on('mpi')
    depends_on('cuda', when='+cuda')

    def configure_args(self):
        spec = self.spec
        config_args = [
            'CC=%s'  % spec['mpi'].mpicc,
            'CXX=%s' % spec['mpi'].mpicxx
        ]

        if '+cuda' in spec:
            config_args.extend([
                '--enable-cuda',
                '--with-cuda=%s' % spec['cuda'].prefix,
            ])

        # librt not available on darwin (and not required)
        if not sys.platform == 'darwin':
            config_args.append('LDFLAGS=-lrt')

        return config_args
