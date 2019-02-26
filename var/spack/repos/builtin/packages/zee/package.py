# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Zee(CMakePackage):

    """Zee is a collection of scalable FEM miniapps based on Omega_h providing
    the basis for an efficient and scalable SSA + E-field client."""

    homepage = "https://github.com/BlueBrain/zee"
    url      = "git@github.com:BlueBrain/zee.git"

    version('develop', git=url, submodules=True)

    variant('build_type', default='', description='CMake build type',
            values=' ')
    variant('optimize', default=True,
            description='Compile C++ with optimization')
    variant('symbols', default=True,
            description='Compile C++ with debug symbols')
    variant('warnings', default=True,
            description='Compile C++ with warnings')
    variant('petsc', default=True,
            description='Compile examples using PETSc')
    depends_on('cmake@3:', type='build')
    depends_on('pkg-config', type='build')
    depends_on('py-cmake-format', type='build', when='@develop')
    depends_on('py-pre-commit', type='build', when='@develop')
    depends_on('py-pyyaml', type='build', when='@develop')
    depends_on('python@3:', type='build', when='@develop')
    depends_on('gmsh@:3 +oce -mpi %gcc')
    depends_on('mpi')
    depends_on('omega-h+trilinos')
    depends_on('petsc +int64', when='+petsc')

    def _bob_options(self):
        cmake_var_prefix = self.name.capitalize() + '_CXX_'
        for variant in ['optimize', 'symbols', 'warnings']:
            cmake_var = cmake_var_prefix + variant.upper()
            if '+' + variant in self.spec:
                yield '-D' + cmake_var + ':BOOL=ON'
            else:
                yield '-D' + cmake_var + ':BOOL=FALSE'
        yield '-DZee_USE_PETSc:BOOL=' + ('TRUE' if '+petsc' in self.spec else 'FALSE')

    def cmake_args(self):
        return list(self._bob_options())
