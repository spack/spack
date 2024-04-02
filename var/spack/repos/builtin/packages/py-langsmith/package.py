# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLangsmith(PythonPackage):
    """Client library to connect to the LangSmith LLM Tracing and Evaluation Platform."""

    pypi = "langsmith/langsmith-0.0.10.tar.gz"

    license("MIT")

    version(
        "0.0.11",
        sha256="c7bdbe28d3fece0eba88e0bd3b85717dbee52399b05a21ccebaa152e5b57e757",
        url="https://pypi.org/packages/67/aa/1a14d85f428281c4e9b2677d299cd49980d2147d3bda3604d2dae2aa1a54/langsmith-0.0.11-py3-none-any.whl",
    )
    version(
        "0.0.10",
        sha256="716412979613a5eb550c9bce33165cd1bad296eb19009040155deccef427ef07",
        url="https://pypi.org/packages/a9/ed/9813d7c199e705865902fdc1e2076b588d6f93ffac93d37f4b50a5205a1b/langsmith-0.0.10-py3-none-any.whl",
    )
    version(
        "0.0.7",
        sha256="9e0ab264b499daa778c694f9129859830820d3fb3a7c93309b630a22b68a88a9",
        url="https://pypi.org/packages/2d/77/d2fbb2155b2683ec3a35ab96e2c32a355615748e31cf9a256341b445900b/langsmith-0.0.7-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:3")
        depends_on("py-pydantic@1.0:1", when="@:0.0.21")
        depends_on("py-requests@2:")
