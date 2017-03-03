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


class Simul(Package):
    """simul is an MPI coordinated test of parallel 
    filesystem system calls and library functions. """

    homepage = "https://github.com/LLNL/simul"
    url      = "https://github.com/LLNL/simul/archive/1.16.tar.gz"

    version('1.16', 'd616c1046a170c1e1b7956c402d23a95')
    version('1.15', 'a5744673c094a87c05c6f0799d1f496f')
    version('1.14', 'f8c14f0bac15741e2af354e3f9a0e30f')
    version('1.13', '8a80a62d569557715d6c9c326e39a8ef')

    depends_on('mpi')

    def install(self, spec, prefix):
        filter_file('mpicc',  '$(MPICC)',  'Makefile', string=True)
        filter_file('inline void',  'void',  'simul.c', string=True)
        make('simul')
        mkdirp(prefix.bin)
        install('simul', prefix.bin)
