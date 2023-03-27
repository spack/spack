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
    url = "https://github.com/NOAA-EMC/UFS_UTILS/archive/refs/tags/ufs_utils_1_6_0.tar.gz"

    maintainers("t-brown", "edwardhartnett", "AlexanderRichert-NOAA", "Hang-Lei-NOAA")

    version("1_6_0", sha256="829ba4b50162e4202f96ec92a65b9fa824f71db65d2b63b70822db07d061cd92")

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
    depends_on("w3nco")
    depends_on("wgrib2")
    depends_on("zlib")

    def cmake_args(self):
        return [
            "-DMPI_C_COMPILER=%s" % self.spec["mpi"].mpicc,
            "-DMPI_Fortran_COMPILER=%s" % self.spec["mpi"].mpifc,
        ]

    def setup_build_environment(self, env):
        env.set("ESMFMKFILE", join_path(self.spec["esmf"].prefix.lib, "esmf.mk"))
