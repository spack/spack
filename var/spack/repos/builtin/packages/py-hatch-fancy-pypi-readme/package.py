# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHatchFancyPypiReadme(PythonPackage):
    """Fancy PyPI READMEs with Hatch."""

    homepage = "https://github.com/hynek/hatch-fancy-pypi-readme"
    pypi = "hatch_fancy_pypi_readme/hatch_fancy_pypi_readme-22.7.0.tar.gz"

    version(
        "23.1.0",
        sha256="9a2c0e5d527611701858083bfb355876f26e04a075342b7d4da725ba5a6dd6ea",
        url="https://pypi.org/packages/6b/74/74a15619861065fa75f6170c649cd2fd5467726bb407ec2017d4a3f92d28/hatch_fancy_pypi_readme-23.1.0-py3-none-any.whl",
    )
    version(
        "22.7.0",
        sha256="4fcdcb4f7d11c7d0fe6b8697345f652250234adfad76b9c8c0c31d29925882a0",
        url="https://pypi.org/packages/bf/14/348c37d4793010c4286a6a7964a5c9c9dbf15ae039552d0e3de21e058e91/hatch_fancy_pypi_readme-22.7.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@22.3:")
        depends_on("py-hatchling")
        depends_on("py-tomli", when="^python@:3.10")
        depends_on("py-typing-extensions", when="@22.3: ^python@:3.7")
