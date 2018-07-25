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


class HoomdBlue(CMakePackage):
    """HOOMD-blue is a general-purpose particle simulation toolkit. It scales
    from a single CPU core to thousands of GPUs.

    You define particle initial conditions and interactions in a high-level
    python script. Then tell HOOMD-blue how you want to execute the job and it
    takes care of the rest. Python job scripts give you unlimited flexibility
    to create custom initialization routines, control simulation parameters,
    and perform in situ analysis."""

    homepage = "http://glotzerlab.engin.umich.edu/hoomd-blue/"
    git      = "https://bitbucket.org/glotzer/hoomd-blue.git"

    version('develop', submodules=True)

    # Bitbucket has tarballs for each release, but they cannot be built.
    # The tarball doesn't come with the git submodules, nor does it come
    # with a .git directory, causing the build to fail. As a workaround,
    # clone a specific tag from Bitbucket instead of using the tarballs.
    # https://bitbucket.org/glotzer/hoomd-blue/issues/238
    version('2.2.2', tag='v2.2.2', submodules=True)
    version('2.1.6', tag='v2.1.6', submodules=True)

    variant('mpi',  default=True,  description='Compile with MPI enabled')
    variant('cuda', default=True,  description='Compile with CUDA Toolkit')
    variant('doc',  default=False, description='Generate documentation')

    # HOOMD-blue requires C++11 support, which is only available in GCC 4.7+
    # https://bitbucket.org/glotzer/hoomd-blue/issues/238
    # https://gcc.gnu.org/projects/cxx-status.html
    conflicts('%gcc@:4.6')

    # HOOMD-blue 2.1.6 uses hexadecimal floats, which are not technically
    # part of the C++11 standard. GCC 6.0+ produces an error when this happens.
    # https://bitbucket.org/glotzer/hoomd-blue/issues/239
    # https://bugzilla.redhat.com/show_bug.cgi?id=1321986
    conflicts('%gcc@6.0:', when='@2.1.6')

    # HOOMD-blue GCC 7+ is not yet supported
    conflicts('%gcc@7.0:')

    extends('python')
    depends_on('python@2.7:')
    depends_on('py-numpy@1.7:', type=('build', 'run'))
    depends_on('cmake@2.8.0:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('cuda@7.0:', when='+cuda')
    depends_on('doxygen@1.8.5:', when='+doc', type='build')

    def cmake_args(self):
        spec = self.spec

        cmake_args = [
            '-DPYTHON_EXECUTABLE={0}'.format(spec['python'].command.path),
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

        return cmake_args
