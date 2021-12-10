##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Synapsetool(CMakePackage):
    """Synapsetool provides a C++ and a python API to read / write neuron
       connectivity informations. Synapsetool is designed to support large
       connectivity data with billions of connections."""
    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/hpc/synapse-tool"
    url      = "ssh://bbpcode.epfl.ch/hpc/synapse-tool"
    git      = "ssh://bbpcode.epfl.ch/hpc/synapse-tool"
    generator = "Ninja"

    version('develop', submodules=True)
    version('0.6.3', tag='v0.6.3', submodules=True)
    version('0.6.2', tag='v0.6.2', submodules=True)
    version('0.6.1', tag='v0.6.1', submodules=True)
    version('0.6.0', tag='v0.6.0', submodules=True)
    version('0.5.9', tag='v0.5.9', submodules=True)
    version('0.5.8', tag='v0.5.8', submodules=True)
    version('0.5.6', tag='v0.5.6', submodules=True)
    version('0.5.5', tag='v0.5.5', submodules=True)
    version('0.5.4', tag='v0.5.4', submodules=True)
    version('0.5.3', tag='v0.5.3', submodules=True)
    version('0.5.2', tag='v0.5.2', submodules=True)
    version('0.5.1', tag='v0.5.1', submodules=True)
    version('0.4.1', tag='v0.4.1', submodules=True)
    version('0.3.3', tag='v0.3.3', submodules=True)
    version('0.2.5', tag='v0.2.5', submodules=True)

    variant('mpi', default=True, description="Enable MPI backend")
    variant('shared', default=True, description="Build shared library")
    variant('python', default=False, description="Enable syntool Python package")

    depends_on('cmake@3.0:', type='build')
    depends_on('ninja', type='build')

    depends_on('boost@1.55:')
    depends_on('mpi',    when='+mpi')
    depends_on('python', when='+python', type=('build', 'run'))
    depends_on('hdf5+mpi', when='+mpi')
    depends_on('hdf5~mpi', when='~mpi')
    depends_on('highfive+mpi', when='+mpi')
    depends_on('highfive~mpi', when='~mpi')
    depends_on('libsonata+mpi', when='+mpi')
    depends_on('libsonata~mpi', when='~mpi')

    patch("tests-unit-cmake.patch", when='@:0.5.6')
    patch("tests-unit-cmake-057.patch", when='@0.5.7:0.5.8')
    patch("fix_highfive_v_2_2_1.patch", when='@:0.5.8^highfive@2.2:')

    def patch(self):
        if self.spec.satisfies('%intel'):
            # Boost just breaks things. Don't use boost for tests.
            filter_file(r'add_subdirectory\(tests\)', '', 'CMakeLists.txt')

    @property
    def libs(self):
        """Export the synapse library
        """
        is_shared = '+shared' in self.spec
        return find_libraries('libsyn2', root=self.prefix, shared=is_shared,
                              recursive=True)

    def dependency_libs(self, spec=None):
        """List of required libraries on linking,
           with the possibility of passing another
           spec where all dependencies have specs.
           This enables Syntool to be external
        """
        spec = spec or self.spec
        is_shared = '+shared' in self.spec['synapsetool']

        boost_libs = ['libboost_system', 'libboost_filesystem']
        if spec['boost'].satisfies('+multithreaded'):
            boost_libs = [lib + '-mt' for lib in boost_libs]

        libraries = (
            find_libraries(boost_libs, spec['boost'].prefix,
                           is_shared, True)
            + find_libraries("libsonata",
                             spec['libsonata'].prefix, is_shared, True)
        )
        return libraries

    def cmake_args(self):
        args = []
        if self.spec.satisfies('+mpi'):
            args.extend([
                '-DCMAKE_C_COMPILER:STRING={0}'.format(self.spec['mpi'].mpicc),
                '-DCMAKE_CXX_COMPILER:STRING={0}'.format(self.spec['mpi'].mpicxx),
                '-DSYNTOOL_WITH_MPI:BOOL=ON',
            ])

        if self.spec.satisfies('~shared'):
            args.append('-DCOMPILE_LIBRARY_TYPE=STATIC')

        return args
