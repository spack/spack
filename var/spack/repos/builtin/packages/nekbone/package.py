##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class Nekbone(Package):
    """NEK5000 emulation software called NEKbone. Nekbone captures the basic
       structure and user interface of the extensive Nek5000 software.
       Nek5000 is a high order, incompressible Navier-Stokes solver based on
       the spectral element method."""

    homepage = "https://github.com/Nek5000/Nekbone"
    url      = "https://github.com/Nek5000/Nekbone/archive/v17.0.tar.gz"
    git      = "https://github.com/Nek5000/Nekbone.git"

    tags = ['proxy-app', 'ecp-proxy-app']

    version('develop', branch='master')
    version('17.0', sha256='ae361cc61368a924398a28a296f675b7f0c4a9516788a7f8fa3c09d787cdf69b')

    # Variants
    variant('mpi', default=True, description='Build with MPI')

    # dependencies
    depends_on('mpi', when='+mpi')

    @run_before('install')
    def fortran_check(self):
        if not self.compiler.fc:
            msg = 'Nekbone can not be built without a Fortran compiler.'
            raise RuntimeError(msg)

    def install(self, spec, prefix):
        mkdir(prefix.bin)

        fc = self.compiler.fc
        cc = self.compiler.cc
        if '+mpi' in spec:
            fc = spec['mpi'].mpif77
            cc = spec['mpi'].mpicc

        # Install Nekbone in prefix.bin
        install_tree(self.stage.source_path, prefix.bin.Nekbone)

        # Install scripts in prefix.bin
        nekpmpi = 'test/example1/nekpmpi'
        makenek = 'test/example1/makenek'

        install(makenek, prefix.bin)
        install(nekpmpi, prefix.bin)

        with working_dir(prefix.bin):
            filter_file(r'^SOURCE_ROOT\s*=.*', 'SOURCE_ROOT=\"' +
                        prefix.bin.Nekbone + '/src\"', 'makenek')
            filter_file(r'^CC\s*=.*', 'CC=\"' + cc + '\"', 'makenek')
            filter_file(r'^F77\s*=.*', 'F77=\"' + fc + '\"', 'makenek')

            if '+mpi' not in spec:
                filter_file(r'^#IFMPI=\"false\"', 'IFMPI=\"false\"', 'makenek')
