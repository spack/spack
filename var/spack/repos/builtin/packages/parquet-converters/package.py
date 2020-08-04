##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class ParquetConverters(CMakePackage):
    """Parquet conversion tools developed by Blue Brain Project, EPFL
    """
    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/building/ParquetConverters"
    url      = "ssh://bbpcode.epfl.ch/building/ParquetConverters"
    git      = "ssh://bbpcode.epfl.ch/building/ParquetConverters"

    version('develop', submodules=True)
    version('0.5.5', tag='v0.5.5', submodules=True)
    version('0.5.4', tag='v0.5.4', submodules=True)
    version('0.5.3', tag='v0.5.3', submodules=True)
    version('0.5.2', tag='v0.5.2', submodules=True)
    version('0.5.1', tag='v0.5.1', submodules=True)
    version('0.5.0', tag='v0.5.0', submodules=True)
    version('0.4.1', tag='v0.4.1')
    version('0.3', tag='v0.3')
    version('0.2.1', tag='v0.2.1')

    depends_on('hdf5+mpi')
    depends_on('highfive+mpi')
    depends_on('arrow+parquet@:0.12', when='@:0.5.5')
    depends_on('arrow+parquet@0.15.1', when='@0.5.6:')
    depends_on('snappy~shared')
    depends_on('synapsetool+mpi')
    depends_on('synapsetool+mpi@:0.5.6', when='@:0.5.2')
    depends_on('mpi')
    depends_on('range-v3', when='@0.4:')

    def cmake_args(self):
        return [
            '-DCMAKE_C_COMPILER={0}'.format(self.spec['mpi'].mpicc),
            '-DCMAKE_CXX_COMPILER={0}'.format(self.spec['mpi'].mpicxx),
            '-DNEURONPARQUET_USE_MPI=ON'
        ]
