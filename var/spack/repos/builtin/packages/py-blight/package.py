# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBlight(PythonPackage):
    """A catch-all compile-tool wrapper."""

    homepage = "https://github.com/trailofbits/blight"
    pypi = "blight/blight-0.0.47.tar.gz"

    maintainers("woodruffw")

    license("Apache-2.0")

    version(
        "0.0.47",
        sha256="6c2c5e4d630992b23fd4165e89af5036662ea62339e97f1df977db86b5203365",
        url="https://pypi.org/packages/36/62/ce130d11c8ee839897851636e9d5de7be46208c30fbd54227b31c12acd3e/blight-0.0.47-py3-none-any.whl",
    )

    variant("dev", default=False, description="Install dependencies to help with development")

    with default_args(type="run"):
        depends_on("python@3.7:")
        depends_on("py-black", when="@0.0.35:0.0.47+dev")
        depends_on("py-click@7.1:", when="@0.0.38:")
        depends_on("py-coverage+toml", when="@0.0.35:0.0.47+dev")
        depends_on("py-flake8", when="@0.0.35:0.0.47+dev")
        depends_on("py-isort", when="@0.0.35:0.0.47+dev")
        depends_on("py-mypy", when="@0.0.35:0.0.47+dev")
        depends_on("py-pdoc3", when="@0.0.35:0.0.47+dev")
        depends_on("py-pydantic@1.7:1", when="@0.0.35:")
        depends_on("py-pytest", when="@0.0.35:0.0.47+dev")
        depends_on("py-pytest-cov", when="@0.0.35:0.0.47+dev")
        depends_on("py-twine", when="@0.0.35:+dev")
        depends_on("py-typing-extensions", when="@0.0.35:")

    # In process of changing build backend after 0.0.47 release.

    # blight uses pyproject.toml to configure isort. isort added
    # support in 5.0.0
