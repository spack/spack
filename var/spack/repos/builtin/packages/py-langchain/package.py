# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLangchain(PythonPackage):
    """Building applications with LLMs through composability"""

    homepage = "https://www.github.com/hwchase17/langchain"
    pypi = "langchain/langchain-0.0.235.tar.gz"

    version("0.0.262", sha256="2cb545cb855ce783f9f272f08a346018b087c0d842012d225ed479ac312624c8")
    version("0.0.235", sha256="6734849e111a4c60e187a1ce7856b31e623604326e48b96601316d108633abd1")
    version("0.0.101", sha256="ee3945c0b8f2d6ba34e5ba63d9362578290269d02999b0049206b508be11e5cc")

    depends_on("python@3.8.1:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
    depends_on("py-pydantic@1", type=("build", "run"))
    depends_on("py-sqlalchemy@1", when="@0.0.101", type=("build", "run"))
    depends_on("py-sqlalchemy@1.4:2", when="@0.0.235:", type=("build", "run"))
    depends_on("py-requests@2", type=("build", "run"))
    depends_on("py-pyyaml@6", when="@0.0.101", type=("build", "run"))
    depends_on("py-pyyaml@5.4.1:", when="@0.0.235:", type=("build", "run"))
    depends_on("py-pyyaml@5.3:", when="@0.0.262:", type=("build", "run"))
    depends_on("py-numpy@1", type=("build", "run"))
    depends_on("py-openapi-schema-pydantic@1.2:1", when="@0.0.235:", type=("build", "run"))
    depends_on("py-dataclasses-json@0.5.7:0.5", type=("build", "run"))
    depends_on("py-tenacity@8.1.0:8", type=("build", "run"))
    depends_on("py-aiohttp@3.8.3:3", type=("build", "run"))
    depends_on("py-numexpr@2.8.4:2", when="@0.0.235:", type=("build", "run"))
    depends_on("py-langsmith@0.0.7", when="@0.0.235", type=("build", "run"))
    depends_on("py-langsmith@0.0.11", when="@0.0.262:", type=("build", "run"))
