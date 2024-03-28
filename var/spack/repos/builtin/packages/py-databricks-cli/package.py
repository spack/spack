# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDatabricksCli(PythonPackage):
    """A command line interface for Databricks."""

    homepage = "https://pypi.org/project/databricks-cli/"
    pypi = "databricks-cli/databricks-cli-0.17.4.tar.gz"

    version(
        "0.17.4",
        sha256="bbd57bc21c88ac6d1f8f0b250db986e500490c4d3cb69664229384632eaeed81",
        url="https://pypi.org/packages/58/7d/4bd6e5dc4420fb5dbb5ae895c1d9934fc0c9e77d9c5dc010725195f093a7/databricks_cli-0.17.4-py2-none-any.whl",
    )
    version(
        "0.14.3",
        sha256="2c628fd9963f30e51646fceab16d64310e4d1f149028117de077259ee383e3ea",
        url="https://pypi.org/packages/a9/44/fc98bde2037fbd1880731a88e2b15f4c8a6d91f88b55ea9c50bf76de8e12/databricks_cli-0.14.3-py2-none-any.whl",
    )
