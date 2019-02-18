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
    version('0.4.1', git=url, tag='v0.4.1', submodules=True, preferred=True)
    version('0.3.3', git=url, tag='v0.3.3', submodules=True)
    version('0.2.5', git=url, tag='v0.2.5', submodules=True)

    variant('mpi', default=True, description="Enable MPI backend")
    variant('shared', default=True, description="Build shared library")
    variant('python', default=False, description="Enable syntool Python package")
    variant('sonata', default=False, description="Enable SONATA support")

    depends_on('boost@1.55:')
    depends_on('cmake@3.0:', type='build')
    depends_on('hdf5+mpi', when='+mpi')
    depends_on('hdf5~mpi', when='~mpi')
    depends_on('highfive+mpi', when='+mpi')
    depends_on('highfive~mpi', when='~mpi')
    depends_on('mpi', when='+mpi')
    depends_on('python', when='+python')

    @property
    def libs(self):
        """Export the synapse library
        """
        is_shared = '+shared' in self.spec
        return find_libraries('libsyn2', root=self.prefix, shared=is_shared, recursive=True)

    def dependency_libs(self, spec=None):
        """List of required libraries on linking, with the possibility of passing another
           spec where all dependencies have specs. This enables Syntool to be external
        """
        spec = spec or self.spec
        is_shared = '+shared' in self.spec['synapsetool']

        boost_libs = ['libboost_system', 'libboost_filesystem']
        if spec['boost'].satisfies('+multithreaded'):
            boost_libs = [l + '-mt' for l in boost_libs]

        libraries = find_libraries(boost_libs, spec['boost'].prefix, is_shared, True)
        if '+sonata' in spec:
            libraries += find_libraries("libsonata", spec['libsonata'].prefix, is_shared, True)
        return libraries

    def cmake_args(self):
        args = []
        spec = self.spec
        if spec.satisfies('+mpi'):
            args.extend([
                '-DCMAKE_C_COMPILER:STRING={}'.format(spec['mpi'].mpicc),
                '-DCMAKE_CXX_COMPILER:STRING={}'.format(spec['mpi'].mpicxx),
                '-DSYNTOOL_WITH_MPI:BOOL=ON',
                '-DSYNTOOL_UNIT_TESTS=OFF'
            ])
        if spec.satisfies('~shared'):
            args.append('-DCOMPILE_LIBRARY_TYPE=STATIC')

        if spec.satisfies('+sonata'):
            args.append('-DSYNTOOL_WITH_SONATA:BOOL=ON')

        return args
