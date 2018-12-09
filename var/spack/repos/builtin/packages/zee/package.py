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
