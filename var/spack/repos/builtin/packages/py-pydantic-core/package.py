# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydanticCore(PythonPackage):
    """Core functionality for Pydantic validation and serialization"""

    homepage = "https://github.com/pydantic/pydantic-core"
    pypi = "pydantic-core/pydantic_core-2.18.2.tar.gz"

    version("2.18.2", sha256="2e29d20810dfc3043ee13ac7d9e25105799817683348823f305ab3f349b9386e")

    depends_on("py-maturin", type="build")
    depends_on("py-typing-extensions@4.6.1:", when="@2:", type=("build", "run"))
