##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Libmesh(AutotoolsPackage):
    """The libMesh library provides a framework for the numerical simulation of
       partial differential equations using arbitrary unstructured
       discretizations on serial and parallel platforms."""

    homepage = "http://libmesh.github.io/"
    url      = "https://github.com/libMesh/libmesh/releases/download/v1.0.0/libmesh-1.0.0.tar.bz2"
    list_url = "https://github.com/libMesh/libmesh/releases"

    version('1.1.0', '92e636163d64cc23762df1cdeec257fe')
    version('1.0.0', 'cb464fc63ea0b71b1e69fa3f5d4f93a4')

    variant('mpi', default=True, description='Enables MPI parallelism')

    depends_on('mpi', when='+mpi')

    # Parallel version of libmesh needs parallel solvers
    depends_on('petsc+mpi', when='+mpi')

    def configure_args(self):
        spec = self.spec
        config_args = []

        if '+mpi' in spec:
            config_args.append('CC={0}'.format(spec['mpi'].mpicc))
            config_args.append('CXX={0}'.format(spec['mpi'].mpicxx))

        return config_args
