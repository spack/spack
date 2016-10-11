##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import os


class Hpx5(Package):
    """The HPX-5 Runtime System. HPX-5 (High Performance ParalleX) is an
    open source, portable, performance-oriented runtime developed at
    CREST (Indiana University). HPX-5 provides a distributed
    programming model allowing programs to run unmodified on systems
    from a single SMP to large clusters and supercomputers with
    thousands of nodes. HPX-5 supports a wide variety of Intel and ARM
    platforms. It is being used by a broad range of scientific
    applications enabling scientists to write code that performs and
    scales better than contemporary runtimes."""
    homepage = "http://hpx.crest.iu.edu"
    url      = "http://hpx.crest.iu.edu/release/hpx-3.1.0.tar.gz"

    version('3.1.0', '9e90b8ac46788c009079632828c77628')
    version('2.0.0', '3d2ff3aab6c46481f9ec65c5b2bfe7a6')
    version('1.3.0', '2260ecc7f850e71a4d365a43017d8cee')
    version('1.2.0', '4972005f85566af4afe8b71afbf1480f')
    version('1.1.0', '646afb460ecb7e0eea713a634933ce4f')
    version('1.0.0', '8020822adf6090bd59ed7fe465f6c6cb')

    variant('debug', default=False, description='Build debug version of HPX-5')
    variant('photon', default=False, description='Enable Photon support')
    variant('mpi', default=False, description='Enable MPI support')

    depends_on("mpi", when='+mpi')
    depends_on("mpi", when='+photon')

    def install(self, spec, prefix):
        extra_args = []
        if '+debug' in spec:
            extra_args.extend([
                '--enable-debug',
                'CFLAGS=-g -O0'
            ])
        else:
            extra_args.append('CFLAGS=-O3')

        if '+mpi' in spec:
            extra_args.append('--enable-mpi')

        if '+photon' in spec:
            extra_args.extend([
                '--enable-mpi',
                '--enable-photon'
            ])

        os.chdir("./hpx/")
        configure('--prefix=%s' % prefix, *extra_args)
        make()
        make("install")
