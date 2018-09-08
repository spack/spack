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


class Libmesh(Package):
    """The libMesh library provides a framework for the numerical simulation of
       partial differential equations using arbitrary unstructured
       discretizations on serial and parallel platforms."""

    homepage = "http://libmesh.github.io/"
    url      = "https://github.com/libMesh/libmesh/releases/download/v1.0.0/libmesh-1.0.0.tar.bz2"
    git      = "https://github.com/libMesh/libmesh.git"

    version('1.3.0', sha256='a8cc2cd44f42b960989dba10fa438b04af5798c46db0b4ec3ed29591b8359786')
    version('1.2.1', sha256='11c22c7d96874a17de6b8c74caa45d6745d40bf3610e88b2bd28fd3381f5ba70')
    version('1.0.0', 'cb464fc63ea0b71b1e69fa3f5d4f93a4')

    variant('mpi', default=True, description='Enables MPI parallelism')
    variant('slepc', default=False, description='SLEPc eigensolver')

    # Parallel version of libMesh needs MPI & parallel solvers
    depends_on('mpi', when='+mpi')
    depends_on('petsc+mpi', when='+mpi')

    # SLEPc version needs SLEPc and requires MPI
    depends_on('slepc', when='+slepc')
    conflicts('~mpi', when='+slepc')

    def install(self, spec, prefix):
        config_args = ["--prefix=%s" % prefix]

        if '+mpi' in spec:
            config_args.append('CC=%s' % spec['mpi'].mpicc)
            config_args.append('CXX=%s' % spec['mpi'].mpicxx)
            config_args.append('PETSC_DIR=%s' % spec['petsc'].prefix)

            if '+slepc' in spec:
                config_args.append('SLEPC_DIR=%s' % spec['slepc'].prefix)

        configure(*config_args)

        make()
        make('install')
