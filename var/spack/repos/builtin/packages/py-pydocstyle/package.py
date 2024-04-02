# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydocstyle(PythonPackage):
    """Python docstring style checker."""

    homepage = "https://github.com/PyCQA/pydocstyle/"
    pypi = "pydocstyle/pydocstyle-6.1.1.tar.gz"

    maintainers("adamjstewart")

    license("MIT")

    version(
        "6.2.1",
        sha256="e034023706489a5786778d21bd25e951052616b260d83e163f09d559dcd647b9",
        url="https://pypi.org/packages/1e/4a/70a55fe6dada5acf640b202a4c2cda39a74cc51222edd44154c914600e9d/pydocstyle-6.2.1-py3-none-any.whl",
    )
    version(
        "6.2.0",
        sha256="39573fa08919ac492b063724af39a1afdcfea8cdaa2c7b8018ca0dfff5d7e36f",
        url="https://pypi.org/packages/90/10/f24113b83880421f62b9d721c4a9f23aca13c0e775d0fdf616927bea813c/pydocstyle-6.2.0-py3-none-any.whl",
    )
    version(
        "6.1.1",
        sha256="6987826d6775056839940041beef5c08cc7e3d71d63149b48e36727f70144dc4",
        url="https://pypi.org/packages/87/67/4df10786068766000518c6ad9c4a614e77585a12ab8f0654c776757ac9dc/pydocstyle-6.1.1-py3-none-any.whl",
    )

    variant("toml", default=True, description="Allow pydocstyle to read pyproject.toml")

    with default_args(type="run"):
        depends_on("py-importlib-metadata@2:4", when="@6.2: ^python@:3.7")
        depends_on("py-snowballstemmer@2.2:", when="@6.2:")
        depends_on("py-snowballstemmer", when="@4:6.1")
        depends_on("py-toml@0.10.2:", when="@6.2:6.2.0+toml")
        depends_on("py-toml", when="@6.1+toml")
        depends_on("py-tomli@1.2.3:", when="@6.2.1:+toml ^python@:3.10")
