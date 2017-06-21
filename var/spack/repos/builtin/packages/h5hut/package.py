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


class H5hut(AutotoolsPackage):
    """H5hut (HDF5 Utility Toolkit).
    High-Performance I/O Library for Particle-based Simulations."""

    homepage = "https://amas.psi.ch/H5hut/"
    url      = "https://amas.psi.ch/H5hut/raw-attachment/wiki/DownloadSources/H5hut-1.99.13.tar.gz"

    version('1.99.13', '2a07a449afe50534de006ac6954a421a')

    variant('fortran', default=True, description='Enable Fortran support')
    variant('mpi',     default=True, description='Enable MPI support')

    depends_on('mpi',                 when='+mpi')
    # h5hut +mpi uses the obsolete function H5Pset_fapl_mpiposix:
    depends_on('hdf5@1.8:1.8.12+mpi', when='+mpi')
    depends_on('hdf5@1.8:',           when='~mpi')

    # If built in parallel, the following error message occurs:
    # install: .libs/libH5hut.a: No such file or directory
    parallel = False

    @run_before('configure')
    def validate(self):
        """Checks if Fortran compiler is available."""

        if '+fortran' in self.spec and not self.compiler.fc:
            raise RuntimeError(
                'Cannot build Fortran variant without a Fortran compiler.')

    def configure_args(self):
        spec = self.spec
        config_args = ['--enable-shared']

        if '+fortran' in spec:
            config_args.append('--enable-fortran')

        if '+mpi' in spec:
            config_args.extend([
                '--enable-parallel',
                'CC={0}'.format(spec['mpi'].mpicc),
                'CXX={0}'.format(spec['mpi'].mpicxx)
            ])

            if '+fortran' in spec:
                config_args.append('FC={0}'.format(spec['mpi'].mpifc))

        return config_args
