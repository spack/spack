# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gsibec(CMakePackage):
    """GSIbec: Extracts the background error covariance (BEC) model
    capabilities from the Gridpoint Statistical Interpolation (GSI)
    atmospheric analysis system into a library of its own."""

    homepage = "https://github.com/GEOS-ESM/gsibec"
    git = "https://github.com/GEOS-ESM/gsibec.git"
    url = "https://github.com/GEOS-ESM/gsibec/archive/refs/tags/1.0.2.tar.gz"

    maintainers = ["mathomp4", "danholdaway"]

    version("develop", branch="develop")
    version("1.0.6", sha256="10e2561685156bcfba35c7799732c77f9c05bd180888506a339540777db833dd")
    version("1.0.5", sha256="ac0cecc59e38da7eefb5a8f27975b33752fa61a4abd3bdbbfb55578ea59d95b3")
    version("1.0.4", sha256="6460e221f2a45640adab016336c070fbe3e7c4b6fc55257945bf5cdb38d5d3e2")
    version("1.0.3", sha256="f104daf55705c5093a3d984073f082017bc9166f51ded36c7f7bb8adf233c916")
    version("1.0.2", sha256="7dc02f1f499e0d9f2843440f517d6c8e5d10ea084cbb2567ec198ba06816bc8b")

    variant("mkl", default=False, description="Use MKL for LAPACK implementation")

    depends_on("mpi", type=("build", "run"))
    depends_on("netcdf-c +mpi", type=("build", "run"))
    depends_on("netcdf-fortran", type=("build", "run"))

    depends_on("mkl", when="+mkl", type=("build", "run"))
    depends_on("lapack", when="~mkl", type=("build", "run"))

    depends_on("ecbuild", type=("build"))
    depends_on("jedi-cmake", type=("build"))
    depends_on("sp", type=("build"))

    def cmake_args(self):
        args = [
            self.define_from_variant("ENABLE_MKL", "mkl"),
        ]
        return args
