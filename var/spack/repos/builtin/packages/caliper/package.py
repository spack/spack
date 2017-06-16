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

class Caliper(CMakePackage):
    """Caliper is a program instrumentation and performance measurement
    framework. It provides data collection mechanisms and a source-code
    annotation API for a variety of performance engineering use cases,
    e.g., performance profiling, tracing, monitoring, and
    auto-tuning.
    """

    homepage = "https://github.com/LLNL/Caliper"
    url      = ""

    version('master', git='https://github.com/LLNL/Caliper.git')

    variant('mpi', default=True, 
            description='Enable MPI wrappers')
    variant('dyninst', default=False, 
            description='Enable symbol translation support with dyninst')
    variant('callpath', default=True,
            description='Enable callpath service (requires libunwind)')
    variant('papi', default=True, description='Enable PAPI service')
    variant('gotcha', default=True, description='Enable GOTCHA support')

    depends_on('dyninst', when='+dyninst')
    depends_on('papi', when='+papi')
    depends_on('mpi', when='+mpi')
    depends_on('libunwind', when='+callpath')

    depends_on('cmake', type='build')
    depends_on('python', type='build')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DBUILD_TESTING=Off',
            '-DWITH_DOCS=Off',
            '-DWITH_TEST_APPS=Off'
        ]

        if '+dyninst' not in spec:
            args.append('-DWITH_DYNINST=Off')
        if '+callpath' not in spec:
            args.append('-DWITH_CALLPATH=Off')
        if '+gotcha' not in spec:
            args.append('-DWITH_GOTCHA=Off')

        if '+papi' in spec:
            args.append('-DPAPI_PREFIX=%s' % spec['papi'].prefix)
        else:
            args.append('-DWITH_PAPI=Off')

        if '+mpi' in spec:
            args.append('-DMPI_C_COMPILER=%s' % spec['mpi'].mpicc)
            args.append('-DMPI_CXX_COMPILER=%s' % spec['mpi'].mpicxx)
        else:
            args.append('-DWITH_MPI=Off')

        return args
