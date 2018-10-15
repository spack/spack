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


class Synapsetool(CMakePackage):
    """Synapsetool provides a C++ and a python API to read / write neuron
       connectivity informations. Synapsetool is designed to support large
       connectivity data with billions of connections."""
    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/hpc/synapse-tool"
    url      = "ssh://bbpcode.epfl.ch/hpc/synapse-tool"

    version('develop', git=url, submodules=True)
    version('0.3.1', git=url, tag='v0.3.1', submodules=True, preferred=True)
    version('0.2.5', git=url, tag='v0.2.5', submodules=True)
    version('0.2.4', git=url, tag='v0.2.4', submodules=True)
    version('0.2.3', git=url, tag='v0.2.3', submodules=True)
    version('0.2.1', git=url, tag='v0.2.1', submodules=True)
    version('0.2.0', git=url, tag='v0.2.0', submodules=True)

    variant('mpi', default=False, description="Enable MPI backend")
    variant('shared', default=True, description="Build shared library")

    depends_on('boost@1.55:')
    depends_on('cmake', type='build')
    depends_on('hdf5+mpi', when='+mpi')
    depends_on('hdf5~mpi', when='~mpi')
    depends_on('highfive+mpi', when='+mpi')
    depends_on('highfive~mpi', when='~mpi')
    depends_on('mpi', when='+mpi')
    depends_on('python')

    @property
    def libs(self):
        """Export the synapse library (especially for neurodamus).
        Sample usage: spec['synapsetool'].libs.ld_flags
        """
        is_shared = '+shared' in self.spec
        libs = find_libraries('libsyn2', root=self.prefix,
                                  shared=is_shared, recursive=True)
        if libs:
            return libs
        return None

    def cmake_args(self):
        args = []
        if self.spec.satisfies('+mpi'):
            args.extend([
                '-DCMAKE_C_COMPILER:STRING={}'.format(self.spec['mpi'].mpicc),
                '-DCMAKE_CXX_COMPILER:STRING={}'.format(self.spec['mpi'].mpicxx),
                '-DSYNTOOL_WITH_MPI:BOOL=ON',
            ])
        if self.spec.satisfies('~shared'):
            args.append('-DCOMPILE_LIBRARY_TYPE=STATIC')
        return args
