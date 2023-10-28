# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLangsmith(PythonPackage):
    """Client library to connect to the LangSmith LLM Tracing and Evaluation Platform."""

    pypi = "langsmith/langsmith-0.0.10.tar.gz"

    version("0.0.11", sha256="7c1be28257d6c7279c85f81e6d8359d1006af3b1238fc198d13ca75c8fe421c8")
    version("0.0.10", sha256="11e5db0d8e29ee5583cabd872eeece8ce50738737b1f52f316ac984f4a1a58c5")
    version("0.0.7", sha256="2f18e51cfd4e42f2b3cf00fa87e9d03012eb7269cdafd8e7c0cf7aa828dcc03e")

    depends_on("python@3.8.1:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
    depends_on("py-pydantic@1", type=("build", "run"))
    depends_on("py-requests@2", type=("build", "run"))
