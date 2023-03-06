# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLaspy(PythonPackage):
    """Native Python ASPRS LAS read/write library."""

    homepage = "https://github.com/laspy/laspy"
    pypi = "laspy/laspy-2.0.3.tar.gz"

    version("2.2.0", sha256="69d36f01acecd719cbe3c3cf58353f247f391ccadb1da37731d45bfe919685df")
    version("2.0.3", sha256="95c6367bc3a7c1e0d8dc118ae4a6b038bf9e8ad3e60741ecb8d59c36d32f822a")

    depends_on("python@3.7:", when="@2.2:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
