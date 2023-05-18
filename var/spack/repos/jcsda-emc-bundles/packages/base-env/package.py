# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class BaseEnv(BundlePackage):
    """Basic development environment used by other environments"""

    homepage = "https://github.com/jcsda/spack-stack"
    git = "https://github.com/jcsda/spack-stack.git"

    maintainers("climbfuji", "AlexanderRichert-NOAA")

    version("1.0.0")

    # Basic utilities
    if sys.platform == "darwin":
        depends_on("libbacktrace", type="run")
    depends_on("cmake", type="run")
    depends_on("git", type="run")
    depends_on("wget", type="run")
    depends_on("curl", type="run")

    # I/O
    depends_on("zlib", type="run")
    depends_on("hdf5", type="run")
    depends_on("netcdf-c", type="run")
    depends_on("netcdf-fortran", type="run")
    depends_on("parallel-netcdf", type="run")
    depends_on("parallelio", type="run")
    depends_on("nccmp", type="run")

    # Python
    depends_on("python@3.7:", type="run")
    depends_on("py-pip", type="run")

    # There is no need for install() since there is no code.
