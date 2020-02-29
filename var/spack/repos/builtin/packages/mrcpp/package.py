# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mrcpp(CMakePackage):
    """The MultiResolution Computation Program Package (MRCPP) is a general purpose
    numerical mathematics library based on multiresolution analysis and the
    multiwavelet basis which provide low-scaling algorithms as well as rigorous
    error control in numerical computations."""

    homepage = "https://mrcpp.readthedocs.io/en/latest/"
    url = "https://github.com/MRChemSoft/mrcpp/archive/v1.1.0.tar.gz"

    maintainers = ["robertodr", "stigrj", "ilfreddy"]

    version('1.2.0-alpha2',
            sha256='8f4df594751a5b7e76b09a62450c6c4956b1974876afa143cc9b5703156ccd40')
    version('1.1.0',
            sha256='e9ffb87eccbd45305f822a0b46b875788b70386b3c1d38add6540dc4e0327ab2',
            preferred=True)
    version('1.0.2',
            sha256='d2b26f7d7b16fa67f16788119abc0f6c7562cb37ece9ba075c116463dcf19df3')
    version('1.0.1',
            sha256='b4d7120545da3531bc7aa0a4cb4eb579fdbe1f8e5d32b1fd1086976583e3e27c')
    version('1.0.0',
            sha256='0858146141d3a60232e8874380390f9e9fa0b1bd6e67099d5833704478213efd')

    variant("openmp", default=True, description="Enable OpenMP support.")

    variant("mpi", default=True, description="Enable MPI support")
    depends_on("mpi", when="+mpi")

    depends_on("cmake@3.11:", type="build")
    depends_on("eigen")

    def cmake_args(self):
        args = [
            "-DENABLE_OPENMP={0}".format("ON" if "+openmp" in
                                         self.spec else "OFF"),
            "-DENABLE_MPI={0}".format("ON" if "+mpi" in self.spec else "OFF"),
        ]
        return args
