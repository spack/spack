# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class FeqParse(CMakePackage):
    """An equation parser Fortran class that
    is used to interpret and evaluate functions
    provided as strings."""

    homepage = "https://github.com/FluidNumerics/feq-parse"
    url = "https://github.com/FluidNumerics/feq-parse/archive/v1.0.0.tar.gz"

    maintainers("fluidnumerics-joe")

    version("1.1.0", sha256="d33a4fd6904939bb70780e8f25f37c1291c4f24fd207feb4ffc0f8d89637d1e3")
    version("1.0.2", sha256="1cd1db7562908ea16fc65dc5268b654405d0b3d9dcfe11f409949c431b48a3e8")

    depends_on("cmake@3.0.2:", type="build")
