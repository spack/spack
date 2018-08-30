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


class Openfast(CMakePackage):
    """Wind turbine simulation package from NREL"""

    homepage = "http://openfast.readthedocs.io/en/latest/"
    git      = "https://github.com/OpenFAST/openfast.git"

    maintainers = ['jrood-nrel']

    version('develop', branch='dev')
    version('master', branch='master')

    variant('shared', default=False,
            description="Build shared libraries")
    variant('double-precision', default=True,
            description="Treat REAL as double precision")
    variant('dll-interface', default=True,
            description="Enable dynamic library loading interface")
    variant('cxx', default=False,
            description="Enable C++ bindings")

    # Dependencies for OpenFAST Fortran
    depends_on('blas')
    depends_on('lapack')

    # Additional dependencies when compiling C++ library
    depends_on('mpi', when='+cxx')
    depends_on('yaml-cpp', when='+cxx')
    depends_on('hdf5+mpi+cxx+hl', when='+cxx')
    depends_on('zlib', when='+cxx')
    depends_on('libxml2', when='+cxx')

    # Disable parallel builds because of OpenFOAM Types modules dependencies
    parallel = False

    def cmake_args(self):
        spec = self.spec

        options = []

        options.extend([
            '-DBUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if '+shared' in spec else 'OFF'),
            '-DDOUBLE_PRECISION:BOOL=%s' % (
                'ON' if '+double-precision' in spec else 'OFF'),
            '-DUSE_DLL_INTERFACE:BOOL=%s' % (
                'ON' if '+dll-interface' in spec else 'OFF'),
            '-DBUILD_FAST_CPP_API:BOOL=%s' % (
                'ON' if '+cxx' in spec else 'OFF'),
        ])

        # Make sure we use Spack's blas/lapack:
        blas_libs = spec['lapack'].libs + spec['blas'].libs
        options.extend([
            '-DBLAS_LIBRARIES=%s' % blas_libs.joined(';'),
            '-DLAPACK_LIBRARIES=%s' % blas_libs.joined(';')
        ])

        if '+cxx' in spec:
            options.extend([
                '-DMPI_CXX_COMPILER:PATH=%s' % spec['mpi'].mpicxx,
                '-DMPI_C_COMPILER:PATH=%s' % spec['mpi'].mpicc,
                '-DMPI_Fortran_COMPILER:PATH=%s' % spec['mpi'].mpifc,
                '-DHDF5_ROOT:PATH=%s' % spec['hdf5'].prefix,
                '-DYAML_ROOT:PATH=%s' % spec['yaml-cpp'].prefix,
            ])

            if '~shared' in spec:
                options.extend([
                    '-DHDF5_USE_STATIC_LIBRARIES=ON',
                ])

        return options
