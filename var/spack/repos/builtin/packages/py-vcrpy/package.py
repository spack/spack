# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVcrpy(PythonPackage):
    """Automatically mock your HTTP interactions to simplify and speed up testing."""

    homepage = "https://github.com/kevin1024/vcrpy"
    pypi = "vcrpy/vcrpy-4.1.1.tar.gz"

    version("4.2.1", sha256="7cd3e81a2c492e01c281f180bcc2a86b520b173d2b656cb5d89d99475423e013")
    version("4.1.1", sha256="57095bf22fc0a2d99ee9674cdafebed0f3ba763018582450706f7d3a74fff599")

    depends_on("python@3.7:", when="@4.2:", type=("build", "run"))
    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-wrapt", type=("build", "run"))
    depends_on("py-six@1.5:", type=("build", "run"))
    depends_on("py-yarl", type=("build", "run"))
