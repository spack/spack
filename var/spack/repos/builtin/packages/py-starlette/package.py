# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyStarlette(PythonPackage):
    """The little ASGI library that shines."""

    homepage = "https://github.com/encode/starlette"
    pypi = "starlette/starlette-0.23.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.27.0",
        sha256="918416370e846586541235ccd38a474c08b80443ed31c578a418e2209b3eef91",
        url="https://pypi.org/packages/58/f8/e2cca22387965584a409795913b774235752be4176d276714e15e1a58884/starlette-0.27.0-py3-none-any.whl",
    )
    version(
        "0.23.1",
        sha256="ec69736c90be8dbfc6ec6800ba6feb79c8c44f9b1706c0b2bb27f936bcf362cc",
        url="https://pypi.org/packages/a3/1d/b23984c05e39ddab35bbba33a3828dc4f896250220dcbd946c0fcad1e934/starlette-0.23.1-py3-none-any.whl",
    )
    version(
        "0.22.0",
        sha256="b5eda991ad5f0ee5d8ce4c4540202a573bb6691ecd0c712262d0bc85cf8f2c50",
        url="https://pypi.org/packages/1d/4e/30eda84159d5b3ad7fe663c40c49b16dd17436abe838f10a56c34bee44e8/starlette-0.22.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.20:0.29")
        depends_on("py-anyio@3.4:", when="@0.19:")
        depends_on("py-typing-extensions@3.10:", when="@0.19: ^python@:3.9")
