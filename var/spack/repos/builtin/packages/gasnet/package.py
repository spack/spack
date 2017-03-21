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


class Gasnet(AutotoolsPackage):
    """GASNet is a language-independent, low-level networking layer
       that provides network-independent, high-performance communication
       primitives tailored for implementing parallel global address space
       SPMD languages and libraries such as UPC, Co-Array Fortran, SHMEM,
       Cray Chapel, and Titanium.
    """
    homepage = "http://gasnet.lbl.gov"
    url      = "http://gasnet.lbl.gov/GASNet-1.24.0.tar.gz"

    version('1.28.2', '6ca0463dc2430570e40646c4d1e97b36')
    version('1.28.0', 'b44446d951d3d8954aa1570e3556ba61')
    version('1.24.0', 'c8afdf48381e8b5a7340bdb32ca0f41a')

    variant('ibv', default=False, description="Support InfiniBand")
    variant('mpi', default=False, description="Support MPI")

    depends_on('mpi', when='+mpi')

    def configure_args(self):
        args = [
            # TODO: factor IB suport out into architecture description.
            "--enable-ibv" if '+ibv' in self.spec else '--disable-ibv',
            "--enable-mpi" if '+mpi' in self.spec else '--disable-mpi',
            "--enable-par",
            "--enable-smp",
            "--enable-udp",
            "--enable-mpi-compat",
            "--enable-smp-safe",
            "--enable-segment-fast",
            "--disable-aligned-segments",
            # TODO: make option so Legion can request builds with/without this.
            # See the Legion webpage for details on when to/not to use.
            "--disable-pshm",
            "--with-segment-mmap-max=64MB",
        ]
        return args
