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


class Psi4(Package):
    """Psi4 is an open-source suite of ab initio quantum chemistry
    programs designed for efficient, high-accuracy simulations of
    a variety of molecular properties."""

    homepage = "http://www.psicode.org/"
    url      = "https://github.com/psi4/psi4/archive/0.5.tar.gz"

    version('0.5', '53041b8a9be3958384171d0d22f9fdd0')

    variant('mpi', default=True, description='Enable MPI parallelization')

    # Required dependencies
    depends_on('python@2.7:')
    depends_on('py-numpy')
    depends_on('blas')
    depends_on('lapack')
    depends_on('cmake@3.0:')
    depends_on('boost@1.55.0:+chrono+filesystem~mpi+python+regex+serialization+system+timer+thread', when='~mpi')
    depends_on('boost@1.55.0:+chrono+filesystem+mpi+python+regex+serialization+system+timer+thread', when='+mpi')

    # Optional dependencies
    depends_on('mpi', when='+mpi')
    # TODO: add packages for these
    # depends_on('perl')
    # depends_on('erd')
    # depends_on('pcm-solver')
    # depends_on('chemps2')

    def install(self, spec, prefix):
        cmake_args = [
            '-DBLAS_TYPE={0}'.format(spec['blas'].name.upper()),
            '-DBLAS_LIBRARIES={0}'.format(spec['blas'].blas_shared_lib),
            '-DLAPACK_TYPE={0}'.format(spec['lapack'].name.upper()),
            '-DLAPACK_LIBRARIES={0}'.format(spec['lapack'].lapack_shared_lib),
            '-DBOOST_INCLUDEDIR={0}'.format(spec['boost'].prefix.include),
            '-DBOOST_LIBRARYDIR={0}'.format(spec['boost'].prefix.lib),
            '-DENABLE_CHEMPS2=OFF'
        ]

        if '+mpi' in spec:
            cmake_args.extend([
                '-DENABLE_MPI=ON'
                #'-DMPI_C_COMPILER={0}'.format(spec['mpi'].mpicc)
                #'-DMPI_C_INCLUDE_PATH={0}'.format(spec['mpi'].prefix.include),
            ])
        else:
            cmake_args.append('-DENABLE_MPI=OFF')

        cmake_args.extend(std_cmake_args)

        with working_dir('spack-build', create=True):
            cmake('..', *cmake_args)

            make()
            #ctest()
            make('install')
