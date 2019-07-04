# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Author: Gilbert Brietzke
# Date: July 2, 2019

from spack import *


class Asagi(CMakePackage):
    """a pArallel Server for Adaptive GeoInformation."""

    homepage = "https://github.com/TUM-I5/ASAGI"
    git = "https://github.com/TUM-I5/ASAGI.git"

    version('1.0.1', commit='f633f96931ae00805f599078d5a1a6a830881554',
            submodules=True, preferred=True)
    version('1.0', commit='f67250798b435c308b9a1e7516f916f7855534ec',
            submodules=True)

    variant('link_type', default='shared',
            description='build shared and/or static libraries',
            values=('static', 'shared'), multi=True)

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

    conflicts('%gcc@5:', when='@:1.0.0')

    def cmake_args(self):

        link_type = self.spec.variants['link_type'].value
        spec = self.spec
        args = ['-DMAX_DIMENSIONS=' + spec.variants['maxDimensions'].value,
                '-DSHARED_LIB=' + ('ON' if 'shared' in link_type else 'OFF'),
                '-DSTATIC_LIB=' + ('ON' if 'static' in link_type else 'OFF'),
                '-DFORTRAN_SUPPORT=' + ('ON' if '+fortran' in spec else 'OFF'),
                '-DTHREADSAFE=' + ('ON' if '+threadsafe' in spec else 'OFF'),
                '-DNOMPI=' + ('ON' if '~mpi' in spec else 'OFF'),
                '-DMPI3=' + ('ON' if '+mpi3' in spec else 'OFF'),
                '-DNONUMA=' + ('ON' if '~numa' in spec else 'OFF'),
                '-DTESTS=' + ('ON' if '+tests' in spec else 'OFF'),
                '-DEXAMPLES=' + ('ON' if '+tests' in spec else 'OFF'),
                '-DTHREADSAFE_COUNTER='
                + ('ON' if '+threadsafeCounter' in spec else 'OFF'),
                '-DTHREADSAFE_MPI='
                + ('ON' if '+threadsafeMPI' in spec else 'OFF'), ]
        return args
