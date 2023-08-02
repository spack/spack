# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Selalib(CMakePackage):
    """Modular library for the kinetic and gyrokinetic simulation of tokamak plasmas by the semi-lagrangian or particle-in-cell methods"""

    homepage = "https://selalib.github.io/selalib"
    url = "https://github.com/selalib/selalib"
    git = "https://github.com/selalib/selalib"

    maintainers = ["pnavaro", "freifrauvonbleifrei"]

    version("main", branch="main")
    
    variant("fmempool", default=False)
    variant("mpi", default=True)
    variant("openmp", default=True)

    depends_on("cmake@3.6.0:", type=("build"))
    depends_on("blas")
    depends_on("fftw+mpi+openmp")
    depends_on("fgsl")
    depends_on("git")
    depends_on("hdf5+fortran+cxx")
    depends_on("mpi+fortran+cxx")
    depends_on("python@3.0.0:")
    depends_on("zfp+fortran")

    def cmake_args(self):
        args = [
            self.define_from_variant("OPENMP_ENABLED", "openmp"),
            self.define_from_variant("HDF5_PARALLEL_ENABLED", "mpi"),
            self.define_from_variant("USE_FMEMPOOOL", "fmempool"),
        ]
        return args
