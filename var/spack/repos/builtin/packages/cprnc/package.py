# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cprnc(CMakePackage):
    """CPRNC is a netcdf file comparison tool used by CESM
    and other scientific programs."""

    url = "https://github.com/ESMCI/cprnc/archive/refs/tags/v1.0.1.tar.gz"
    homepage = "https://github.com/ESMCI/cprnc"

    maintainers("jedwards4b", "billsacks")

    version("1.0.1", sha256="19517b52688f5ce40c385d7a718e06bf88a8731335943bc32e2b8410c489d6eb")

    depends_on("netcdf-fortran")
    depends_on("cmake@3:", type="build")
