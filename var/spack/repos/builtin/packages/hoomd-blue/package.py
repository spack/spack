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
import os


class HoomdBlue(Package):
    """HOOMD-blue is a general-purpose particle simulation toolkit. It scales
    from a single CPU core to thousands of GPUs.

    You define particle initial conditions and interactions in a high-level
    python script. Then tell HOOMD-blue how you want to execute the job and it
    takes care of the rest. Python job scripts give you unlimited flexibility
    to create custom initialization routines, control simulation parameters,
    and perform in situ analysis."""

    homepage = "https://codeblue.umich.edu/hoomd-blue/index.html"
    url      = "https://bitbucket.org/glotzer/hoomd-blue/get/v1.3.3.tar.bz2"

    version('1.3.3', '1469ef4531dc14b579c0acddbfe6a273')

    variant('mpi',  default=True, description='Compile with MPI enabled')
    variant('cuda', default=True, description='Compile with CUDA Toolkit')
    variant('doc',  default=True, description='Generate documentation')

    extends('python')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('boost+python')
    depends_on('cmake', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('cuda', when='+cuda')
    depends_on('doxygen', when='+doc', type='build')

    def install(self, spec, prefix):

        cmake_args = [
            '-DPYTHON_EXECUTABLE=%s/python' % spec['python'].prefix.bin,
            '-DBOOST_ROOT=%s'               % spec['boost'].prefix
        ]

        # MPI support
        if '+mpi' in spec:
            os.environ['MPI_HOME'] = spec['mpi'].prefix
            cmake_args.append('-DENABLE_MPI=ON')
        else:
            cmake_args.append('-DENABLE_MPI=OFF')

        # CUDA support
        if '+cuda' in spec:
            cmake_args.append('-DENABLE_CUDA=ON')
        else:
            cmake_args.append('-DENABLE_CUDA=OFF')

        # CUDA-aware MPI library support
        # if '+cuda' in spec and '+mpi' in spec:
        #    cmake_args.append('-DENABLE_MPI_CUDA=ON')
        # else:
        #    cmake_args.append('-DENABLE_MPI_CUDA=OFF')

        # There may be a bug in the MPI-CUDA code. See:
        # https://groups.google.com/forum/#!msg/hoomd-users/2griTESmc5I/E69s_M5fDwAJ
        # This prevented "make test" from passing for me.
        cmake_args.append('-DENABLE_MPI_CUDA=OFF')

        # Documentation
        if '+doc' in spec:
            cmake_args.append('-DENABLE_DOXYGEN=ON')
        else:
            cmake_args.append('-DENABLE_DOXYGEN=OFF')

        cmake_args.extend(std_cmake_args)
        cmake('.', *cmake_args)

        make()
        make("test")
        make("install")
