# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMonkeytype(PythonPackage):
    """Generating type annotations from sampled production types."""

    homepage = "https://github.com/instagram/MonkeyType"
    pypi = "MonkeyType/MonkeyType-22.2.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "22.2.0",
        sha256="3d0815c7e98a18e9267990a452548247f6775fd636e65df5a7d77100ea7ad282",
        url="https://pypi.org/packages/0c/40/2ce3488035207c0a2acb9c9d101a80bbb274e27138a09f5a39445c6c3faf/MonkeyType-22.2.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-libcst@0.3.7:", when="@21:22")
        depends_on("py-mypy-extensions", when="@19.11.1:20.4.2.0,20.5:")
