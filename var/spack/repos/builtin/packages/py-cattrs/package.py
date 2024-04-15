# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCattrs(PythonPackage):
    """An open source Python library for structuring and unstructuring data."""

    homepage = "https://github.com/python-attrs/cattrs"
    pypi = "cattrs/cattrs-22.2.0.tar.gz"

    license("MIT")

    version(
        "22.2.0",
        sha256="bc12b1f0d000b9f9bee83335887d532a1d3e99a833d1bf0882151c97d3e68c21",
        url="https://pypi.org/packages/43/3b/1d34fc4449174dfd2bc5ad7047a23edb6558b2e4b5a41b25a8ad6655c6c7/cattrs-22.2.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@22.2:23.1")
        depends_on("py-attrs@20:", when="@1.8:23.1")
        depends_on("py-exceptiongroup", when="@22.2:23.1 ^python@:3.10")
        depends_on("py-typing-extensions", when="@22.2:22 ^python@:3.7")
