# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Zee(CMakePackage):

    """Zee is a collection of scalable FEM miniapps based on Omega_h providing
    the basis for an efficient and scalable SSA + E-field client."""

    homepage = "https://github.com/BlueBrain/zee"
    url      = "git@github.com:BlueBrain/zee.git"
    git      = "git@github.com:BlueBrain/zee.git"

    version('develop', submodules=True)
    version('0.0.1-dev0', commit='358e75347ac69da91fb2fab309ce85f705f6e4dd', submodules=True)

    variant('build_type', default=' ', description='CMake build type',
            values=' ')
    variant('optimize', default=True,
            description='Compile C++ with optimization')
    variant('symbols', default=True,
            description='Compile C++ with debug symbols')
    variant('warnings', default=True,
            description='Compile C++ with warnings')
    variant('petsc', default=True,
            description='Compile examples using PETSc')
    variant('opsplit-only', default=False,
            description='Only build operator splitting clients')
    variant('codechecks', default=False,
            description='Perform additional code checks like ' +
                        'formatting or static analysis')
    variant('timemory', default=False,
            description='Add timemory API for time/memory measurement')

    depends_on('benchmark')
    depends_on('boost')
    depends_on('cgal')
    depends_on('cmake@3:', type='build')
    depends_on('pkg-config', type='build')
    depends_on('git', type='build', when='+codechecks')
    depends_on('igraph')
    depends_on('py-cmake-format', type='build', when='+codechecks')
    depends_on('py-pre-commit', type='build', when='+codechecks')
    depends_on('py-pyyaml', type='build', when='+codechecks')
    depends_on('python@3:', type='build', when='+codechecks')
    depends_on('gmsh@4: +metis~mpi+oce+openmp+shared')
    depends_on('mpi')
    depends_on('omega-h+gmsh')

    depends_on('metis+int64')
    depends_on('petsc +int64', when='+petsc')
    depends_on('timemory', when='+timemory')

    def _bob_options(self):
        cmake_var_prefix = self.name.capitalize() + '_CXX_'
        for variant in ['optimize', 'symbols', 'warnings']:
            cmake_var = cmake_var_prefix + variant.upper()
            if '+' + variant in self.spec:
                yield '-D' + cmake_var + ':BOOL=ON'
            else:
                yield '-D' + cmake_var + ':BOOL=FALSE'
        yield '-DZee_OPSPLIT_CLIENTS_ONLY:BOOL=' + \
            ('TRUE' if '+opsplit-only' in self.spec else 'FALSE')
        yield '-DZee_USE_PETSc:BOOL=' + \
            ('TRUE' if '+petsc' in self.spec else 'FALSE')
        if '+codechecks' in self.spec:
            yield '-DPYTHON_EXECUTABLE:FILEPATH=' + \
                self.spec['python'].command.path
            yield '-DZee_FORMATTING:BOOL=TRUE'
            yield '-DZee_TEST_FORMATTING:BOOL=TRUE'
        if '+timemory' in self.spec:
            yield '-DZee_USE_TIMEMORY:BOOL=ON'

    def cmake_args(self):
        return list(self._bob_options())
