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


class BerkeleyUpc(AutotoolsPackage):
    """Unified Parallel C (UPC) is an extension of the C programming language
    designed for high performance computing on large-scale parallel
    machines."""

    homepage = "http://upc.lbl.gov/"
    url      = "http://upc.lbl.gov/download/release/berkeley_upc-2.26.0.tar.gz"

    version('2.26.0', 'd73f46c4f7a8d124781097e2bab28184')

    depends_on('mpi')

    conflicts('%gcc@7.1.0')

    @property
    def build_directory(self):
        return join_path(self.stage.source_path, 'build')

    def configure_args(self):
        args = ['CC=%s' % spack_cc,
                'CXX=%s' % spack_cxx,
                'MPI_CC=%s' % self.spec['mpi'].mpicc,
                '--disable-ibv',
                '--enable-pthreads',
                '--enable-udp',
                '--enable-mpi',
                '--enable-smp',
                '--with-default-network=smp',
                '--enable-pshm'
                ]
        return args
