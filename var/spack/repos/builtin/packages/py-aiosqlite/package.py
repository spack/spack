# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAiosqlite(PythonPackage):
    """asyncio bridge to the standard sqlite3 module"""

    homepage = "https://aiosqlite.omnilib.dev"
    pypi = "aiosqlite/aiosqlite-0.17.0.tar.gz"

    license("MIT")

    version(
        "0.17.0",
        sha256="6c49dc6d3405929b1d08eeccc72306d3677503cc5e5e43771efc1e00232e8231",
        url="https://pypi.org/packages/a0/48/77c0092f716c4bf9460dca44f5120f70b8f71f14a12f40d22551a7152719/aiosqlite-0.17.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-typing-extensions@3.7:", when="@0.16:0.17")

    # aiosqlite.test requires aiounittests, not yet in spack
    import_modules = ["aiosqlite"]
