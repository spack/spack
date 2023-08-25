# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Netcdf95(CMakePackage):
    """NetCDF95 is an alternative Fortran interface to the NetCDF library
    which uses Fortran 2003 features."""

    homepage = "https://lguez.github.io/NetCDF95/"
    git = "https://github.com/lguez/NetCDF95.git"

    maintainers("RemiLacroix-IDRIS")

    version("0.3", tag="v0.3", submodules=True)

    depends_on("netcdf-fortran")
