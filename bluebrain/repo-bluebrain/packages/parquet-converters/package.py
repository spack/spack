##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class ParquetConverters(CMakePackage):
    """Parquet conversion tools developed by Blue Brain Project, EPFL
    """
    homepage = "https://bbpgitlab.epfl.ch/hpc/circuit-building/parquet-converters"
    url      = "git@bbpgitlab.epfl.ch:hpc/circuit-building/parquet-converters.git"
    git      = "git@bbpgitlab.epfl.ch:hpc/circuit-building/parquet-converters.git"

    version('develop', submodules=True)
    version('0.7.0', tag='v0.7.0', submodules=True)
    version('0.6.1', tag='v0.6.1', submodules=True)
    version('0.5.7', tag='v0.5.7', submodules=True)
    version('0.4.1', tag='v0.4.1')
    version('0.3', tag='v0.3')
    version('0.2.1', tag='v0.2.1')

    depends_on('hdf5+mpi')
    depends_on('highfive+mpi')
    depends_on('arrow+parquet@:0.12', when='@:0.5.5')
    depends_on('arrow+parquet@0.15.1', when='@0.5.6:0.5.7')
    depends_on('arrow+parquet@3.0.0:', when='@0.6.0:')
    depends_on('snappy~shared')
    depends_on('synapsetool+mpi')
    depends_on('synapsetool+mpi@:0.5.6', when='@:0.5.2')
    depends_on('mpi')
    depends_on('range-v3@:0.10', when='@0.4:')

    def cmake_args(self):
        return [
            '-DCMAKE_C_COMPILER={0}'.format(self.spec['mpi'].mpicc),
            '-DCMAKE_CXX_COMPILER={0}'.format(self.spec['mpi'].mpicxx),
            '-DNEURONPARQUET_USE_MPI=ON'
        ]
