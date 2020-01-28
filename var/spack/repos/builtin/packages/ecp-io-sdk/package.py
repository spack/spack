# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class EcpIoSdk(CMakePackage):
    """ECP I/O Services SDK"""

    homepage = "https://github.com/chuckatkins/ecp-data-viz-sdk"
    git      = "https://github.com/chuckatkins/ecp-data-viz-sdk.git"

    maintainers = ['chuckatkins']

    version('1.0', branch='master')

    variant('adios2', default=True, description="Enable ADIOS2")
    variant('darshan', default=True, description="Enable Darshan")
    variant('faodel', default=False, description="Enable FAODEL")
    variant('hdf5', default=True, description="Enable HDF5")
    variant('mercury', default=True, description="Enable Mercury")
    variant('pnetcdf', default=True, description="Enable PNetCDF")
    variant('unifyfs', default=True, description="Enable UnifyFS")
    variant('veloc', default=True, description="Enable VeloC")

    # Currently no spack packages
    # variant('romio', default=False, description="Enable ROMIO")

    depends_on('adios2+mpi+fortran+zfp+hdf5', when='+adios2')
    depends_on('darshan-runtime', when='+darshan')
    depends_on('darshan-util', when='+darshan')
    depends_on('faodel+mpi+hdf5', when='+faodel')
    depends_on('hdf5+mpi+fortran', when='+hdf5')
    depends_on('mercury+mpi+ofi+sm', when='+mercury')
    depends_on('parallel-netcdf+fortran+pic', when='+pnetcdf')
    depends_on('unifyfs+fortran+numa', when='+unifyfs')
    depends_on('veloc', when='+veloc')

    def cmake_args(self):
        return ['-DIO=ON']
