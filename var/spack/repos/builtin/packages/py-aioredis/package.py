# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAioredis(PythonPackage):
    """asyncio (PEP 3156) Redis support."""

    homepage = "https://github.com/aio-libs/aioredis"
    pypi = "aioredis/aioredis-1.3.1.tar.gz"

    license("MIT")

    version(
        "1.3.1",
        sha256="b61808d7e97b7cd5a92ed574937a079c9387fdadd22bfbfa7ad2fd319ecc26e3",
        url="https://pypi.org/packages/b0/64/1b1612d0a104f21f80eb4c6e1b6075f2e6aba8e228f46f229cfd3fdac859/aioredis-1.3.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-async-timeout", when="@1:")
        depends_on("py-hiredis", when="@:1")
