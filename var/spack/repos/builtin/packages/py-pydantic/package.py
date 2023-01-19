# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydantic(PythonPackage):
    """Data validation and settings management using Python type hinting."""

    homepage = "https://github.com/samuelcolvin/pydantic"
    pypi = "pydantic/pydantic-1.8.2.tar.gz"

    version("1.10.2", sha256="91b8e218852ef6007c2b98cd861601c6a09f1aa32bbbb74fab5b1c33d4a1e410")
    version("1.9.2", sha256="8cb0bc509bfb71305d7a59d00163d5f9fc4530f0881ea32c74ff4f74c85f3d3d")
    version("1.8.2", sha256="26464e57ccaafe72b7ad156fdaa4e9b9ef051f69e175dbbb463283000c05ab7b")

    variant("dotenv", default=False, description="Install requirements for pydantic.dotenv")

    depends_on("python@3.7:", when="@1.10.2:", type=("build", "run"))
    depends_on("python@3.6.1:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-typing-extensions@4.1.0:", when="@1.10.2:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4.3:", type=("build", "run"))

    depends_on("py-python-dotenv@0.10.4:", when="+dotenv", type=("build", "run"))
