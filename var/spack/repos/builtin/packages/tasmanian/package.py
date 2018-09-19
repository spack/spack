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


class Tasmanian(CMakePackage):
    """The Toolkit for Adaptive Stochastic Modeling and Non-Intrusive
    ApproximatioN is a robust library for high dimensional integration and
    interpolation as well as parameter calibration."""

    homepage = 'http://tasmanian.ornl.gov'
    url      = 'https://github.com/ORNL/TASMANIAN/archive/v5.1.tar.gz'
    git      = 'https://github.com/ORNL/TASMANIAN.git'

    version('xsdk-0.3.0', branch='master')
    version('develop', branch='master')

    version('5.1', '5d904029a24470a6acf4a87d3339846e')

    version('5.0', '4bf131841d786033863d271739be0f7a',
            url='http://tasmanian.ornl.gov/documents/Tasmanian_v5.0.zip')

    variant('xsdkflags', default=False,
            description='enable XSDK defaults for Tasmanian')

    variant('openmp', default=True,
            description='add OpenMP support to Tasmanian')
    # tested with OpenMP 3.1 (clang4) through 4.0-4.5 (gcc 5 - 8)

    variant('blas', default=False,
            description='add BLAS support to Tasmanian')

    variant('mpi', default=False,
            description='add MPI support to Tasmanian')

    variant('cuda', default=False,
            description='add CUDA support to Tasmanian')

    variant('magma', default=False,
            description='add UTK MAGMA support to Tasmanian')

    variant('python', default=False,
            description='add Python binding for Tasmanian')

    depends_on('cmake@3.5.0:', type='build')

    depends_on('python@2.7:', when='+python', type=('build', 'run'))
    depends_on('py-numpy', when='+python', type=('build', 'run'))

    extends('python', when='+python')

    depends_on('mpi', when="+mpi")  # openmpi 2 and 3 tested

    depends_on('blas', when="+blas")  # openblas 0.2.18 or newer

    depends_on('cuda@9.1', when='+cuda', type=('build', 'run'))
    depends_on('cuda@9.1', when='+magma', type=('build', 'run'))

    depends_on('magma@2.3.0', when='+magma', type=('build', 'run'))

    def cmake_args(self):
        spec = self.spec

        if '+xsdkflags' in spec:
            args = [
                '-DUSE_XSDK_DEFAULTS:BOOL=ON',
                '-DXSDK_ENABLE_PYTHON:BOOL={0}'.format(
                    'ON' if '+python' in spec else 'OFF'),
                '-DTasmanian_ENABLE_MPI:BOOL={0}'.format(
                    'ON' if '+mpi' in spec else 'OFF'),
                '-DXSDK_ENABLE_OPENMP:BOOL={0}'.format(
                    'ON' if '+openmp' in spec else 'OFF'),
                '-DTPL_ENABLE_BLAS:BOOL={0}'.format(
                    'ON' if '+blas' in spec else 'OFF'),
                '-DXSDK_ENABLE_CUDA:BOOL={0}'.format(
                    'ON' if '+cuda' in spec else 'OFF'),
                '-DXSDK_ENABLE_CUDA:BOOL={0}'.format(
                    'ON' if '+magma' in spec else 'OFF'),
                '-DTPL_ENABLE_MAGMA:BOOL={0}'.format(
                    'ON' if '+magma' in spec else 'OFF'), ]
        else:
            args = [
                '-DTasmanian_ENABLE_OPENMP:BOOL={0}'.format(
                    'ON' if '+openmp' in spec else 'OFF'),
                '-DTasmanian_ENABLE_BLAS:BOOL={0}'.format(
                    'ON' if '+blas' in spec else 'OFF'),
                '-DTasmanian_ENABLE_PYTHON:BOOL={0}'.format(
                    'ON' if '+python' in spec else 'OFF'),
                '-DTasmanian_ENABLE_MPI:BOOL={0}'.format(
                    'ON' if '+mpi' in spec else 'OFF'),
                '-DTasmanian_ENABLE_CUDA:BOOL={0}'.format(
                    'ON' if '+cuda' in spec else 'OFF'),
                '-DTasmanian_ENABLE_CUDA:BOOL={0}'.format(
                    'ON' if '+magma' in spec else 'OFF'),
                '-DTasmanian_ENABLE_MAGMA:BOOL={0}'.format(
                    'ON' if '+magma' in spec else 'OFF'), ]

        if spec.satisfies('+python'):
            args.append('-DPYTHON_EXECUTABLE:FILEPATH={0}'.format(
                self.spec['python'].command.path))
        return args
