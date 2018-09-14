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


class Gasnet(AutotoolsPackage):
    """GASNet is a language-independent, low-level networking layer
       that provides network-independent, high-performance communication
       primitives tailored for implementing parallel global address space
       SPMD languages and libraries such as UPC, Co-Array Fortran, SHMEM,
       Cray Chapel, and Titanium.
    """
    homepage = "http://gasnet.lbl.gov"
    url      = "http://gasnet.lbl.gov/download/GASNet-1.24.0.tar.gz"

    version('1.32.0', sha256='42e4774b3bbc7c142f77c41b6ce86b594f579073f46c31f47f424c7e31ee1511')
    version('1.30.0', '2ddb1d8397d62acfd389095ca8da72f6')
    version('1.28.2', '6ca0463dc2430570e40646c4d1e97b36')
    version('1.28.0', 'b44446d951d3d8954aa1570e3556ba61')
    version('1.24.0', 'c8afdf48381e8b5a7340bdb32ca0f41a')

    variant('ibv', default=False, description="Support InfiniBand")
    variant('mpi', default=True, description="Support MPI")
    variant('aligned-segments', default=False,
            description="Requirement to achieve aligned VM segments")
    variant('pshm', default=True, 
            description="Support inter-process shared memory support")
    variant('segment-mmap-max', default='16GB',
            description="Upper bound for mmap-based GASNet segments")

    conflicts('+aligned-segments', when='+pshm')

    depends_on('mpi', when='+mpi')

    def configure_args(self):
        args = [
            # TODO: factor IB suport out into architecture description.
            "--enable-ibv" if '+ibv' in self.spec else '--disable-ibv',
            "--enable-par",
            "--enable-smp",
            "--enable-udp",
            "--enable-smp-safe",
            "--enable-segment-fast",
            "--enable-pshm" if '+pshm' in self.spec else "--disable-pshm",
            "--with-segment-mmap-max={0}".format(
                self.spec.variants['segment-mmap-max'].value),
            # for consumers with shared libs
            "CC=%s %s" % (spack_cc, self.compiler.pic_flag),
            "CXX=%s %s" % (spack_cxx, self.compiler.pic_flag),
        ]

        if '+aligned-segments' in self.spec:
            args.append('--enable-aligned-segments')
        else:
            args.append('--disable-aligned-segments')

        if '+mpi' in self.spec:
            args.extend(['--enable-mpi', '--enable-mpi-compat', "MPI_CC=%s %s"
                        % (self.spec['mpi'].mpicc, self.compiler.pic_flag)])
        else:
            args.extend(['--disable-mpi', '--disable-mpi-compat'])
        return args
