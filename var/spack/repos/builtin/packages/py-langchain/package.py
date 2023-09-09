# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLangchain(PythonPackage):
    """Building applications with LLMs through composability"""

    homepage = "https://www.github.com/langchain-ai/langchain"
    pypi = "langchain/langchain-0.0.285.tar.gz"

    maintainers("julianolm")

    version("0.0.285", sha256="68940dcffa63c6245e8986146614d3ce2eb22fec96ae831ed0cce97ccba3d427")

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-setuptools")
    depends_on("py-pytest")

    depends_on("py-langsmith", type=("build", "run"))
    depends_on("py-aiohttp", type=("build", "run"))
    depends_on("py-async-timeout", type=("build", "run"))
    depends_on("py-pydantic", type=("build", "run"))
    depends_on("py-dataclasses-json", type=("build", "run"))
    depends_on("py-sqlalchemy", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-tenacity", type=("build", "run"))
    depends_on("py-numexpr", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
