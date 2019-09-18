# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    variant('hdf5', default=True, description="Enable HDF5")
    variant('adios2', default=True, description="Enable ADIOS2")
    variant('pnetcdf', default=True, description="Enable PNetCDF")
    variant('darshan', default=True, description="Enable Darshan")
    variant('mercury', default=True, description="Enable Mercury")
    variant('unifyfs', default=True, description="Enable UnifyFS")
    variant('veloc', default=True, description="Enable VeloC")

    # Currently no spack packages
    # variant('romio', default=False, description="Enable ROMIO")
    # variant('faodel', default=False, description="Enable FAODEL")

    depends_on('hdf5', when='+hdf5')
    depends_on('adios2', when='+adios2')
    depends_on('parallel-netcdf', when='+pnetcdf')
    depends_on('veloc', when='+veloc')
    depends_on('unifyfs', when='+unifyfs')
    depends_on('darshan-runtime', when='+darshan')
    depends_on('darshan-util', when='+darshan')
    depends_on('mercury', when='+mercury')

    def cmake_args(self):
        return ['-DIO=ON']
