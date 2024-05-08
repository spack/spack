##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class ParquetConverters(CMakePackage):
    """Parquet conversion tools developed by Blue Brain Project, EPFL"""

    homepage = "https://bbpgitlab.epfl.ch/hpc/circuit-building/parquet-converters"
    url = "ssh://git@bbpgitlab.epfl.ch/hpc/circuit-building/parquet-converters.git"
    git = "ssh://git@bbpgitlab.epfl.ch/hpc/circuit-building/parquet-converters.git"

    submodules = True

    version("develop", branch="main")
    version("0.8.1", tag="v0.8.1")
    version("0.8.0", tag="v0.8.0")
    version("0.7.0", tag="v0.7.0")
    version("0.6.1", tag="v0.6.1")
    version("0.5.7", tag="v0.5.7")

    depends_on("hdf5+mpi")
    depends_on("highfive+mpi")
    depends_on("arrow+parquet+snappy@:0.12", when="@:0.5.5")
    depends_on("arrow+parquet+snappy@0.15.1", when="@0.5.6:0.5.7")
    depends_on("arrow+parquet+snappy@3.0.0:", when="@0.6.0:")
    depends_on("nlohmann-json", when="@0.7.1:")
    depends_on("synapsetool+mpi", when="@:0.8")
    depends_on("mpi")
    depends_on("range-v3@:0.10", when="@0.4:0.8")
    depends_on("range-v3@0.11:", when="@0.9:")
    depends_on("catch2", when="@0.9:")

    def cmake_args(self):
        return [
            self.define("CMAKE_C_COMPILER", self.spec["mpi"].mpicc),
            self.define("CMAKE_CXX_COMPILER", self.spec["mpi"].mpicxx),
            self.define("NEURONPARQUET_USE_MPI", True),
        ]
