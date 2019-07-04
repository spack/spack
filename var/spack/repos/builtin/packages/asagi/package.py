# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# Author: Gilbert Brietzke
# Date: July 2, 2019

from spack import *


class Asagi(CMakePackage):
    """a pArallel Server for Adaptive GeoInformation."""

    homepage = "https://github.com/TUM-I5/ASAGI"
    git = "https://github.com/TUM-I5/ASAGI.git"

    version('f633f96', commit='f633f96931ae00805f599078d5a1a6a830881554',
            submodules=True, preferred=True)

    variant('shared', default=True, description="enable shared libraries")
    variant('static', default=False, description="enable static libraries")
    variant('fortran', default=True, description="enable fortran support")
    variant('maxDimensions', default=4,
            description="max. number of dimensions supported")
    variant('numa', default=True, description="enable NUMA support")
    variant('mpi', default=True, description="enable MPI")
    variant('threadsafe', default=True,
            description="enable threadsafe ASAGI-functions")
    variant('threadsafeCounter', default=False,
            description="enable threadsafe access counters")
    variant('threadsafeMPI', default=True,
            description="make MPI calls threadsafe")
    variant('mpi3', default=True,
            description="enable MPI-3 (enables additional features)")
    variant('tests', default=False, description="compile tests")
    variant('examples', default=False, description="compile examples")

    depends_on('mpi', when="+mpi")
    depends_on('mpi@3:', when="+mpi3")
    depends_on('netcdf +mpi', when="+mpi")
    depends_on('netcdf ~mpi', when="~mpi")
    depends_on('numactl', when="+numa")

    def cmake_args(self):

        args = []

        args.append('-DMAX_DIMENSIONS=' +
                    self.spec.variants['maxDimensions'].value)

        if '~shared' in self.spec:
            args.append('-DSHARED_LIB=OFF')

        if '+static' in self.spec:
            args.append('-DSTATIC_LIB=ON')

        if '~fortran' in self.spec:
            args.append('-DFORTRAN_SUPPORT=OFF')

        if '~threadsafe' in self.spec:
            args.append('-DTHREADSAFE=OFF')

        if '+threadsafeCounter' in self.spec:
            args.append('-DTHREADSAFE_COUNTER=ON')

        if '~threadsafeMPI' in self.spec:
            args.append('-DTHREADSAFE_MPI=OFF')

        if '~mpi' in self.spec:
            args.append('-DNOMPI=ON')

        if '~mpi3' in self.spec:
            args.append('-DMPI3=OFF')

        if '~numa' in self.spec:
            args.append('-DNONUMA=ON')

        if '+tests' in self.spec:
            args.append('-DTESTS=ON')

        if '+examples' in self.spec:
            args.append('-DEXAMPLES=ON')

        return args
