# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UfsUtils(CMakePackage):
    """The UFS Utilities package contains programs set up the model grid and
    create coldstart initial conditions.

    This is related to NOAA's NCEPLIBS project."""

    homepage = "https://noaa-emcufs-utils.readthedocs.io/en/latest/"
    url = "https://github.com/NOAA-EMC/UFS_UTILS/archive/refs/tags/ufs_utils_1_7_0.tar.gz"
    git = "https://github.com/ufs-community/UFS_UTILS"

    maintainers("t-brown", "edwardhartnett", "AlexanderRichert-NOAA", "Hang-Lei-NOAA")

    version("1.10.0", tag="ufs_utils_1_10_0", submodules=True)
    version("1.9.0", tag="ufs_utils_1_9_0", submodules=True)
    version("1.8.0", tag="ufs_utils_1_8_0", submodules=True)
    version("1.7.0", tag="ufs_utils_1_7_0", submodules=True)

    depends_on("mpi")
    depends_on("cmake@3.23:")
    depends_on("bacio")
    depends_on("esmf")
    depends_on("g2")
    depends_on("hdf5")
    depends_on("ip")
    depends_on("jasper")
    depends_on("libpng")
    depends_on("nemsio")
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("sfcio")
    depends_on("sigio")
    depends_on("sp")
    depends_on("w3emc")
    depends_on("zlib")

    def cmake_args(self):
        return [
            "-DMPI_C_COMPILER=%s" % self.spec["mpi"].mpicc,
            "-DMPI_Fortran_COMPILER=%s" % self.spec["mpi"].mpifc,
        ]

    def setup_build_environment(self, env):
        env.set("ESMFMKFILE", join_path(self.spec["esmf"].prefix.lib, "esmf.mk"))
