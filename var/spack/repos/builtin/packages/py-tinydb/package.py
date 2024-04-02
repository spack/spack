# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTinydb(PythonPackage):
    """TinyDB is a tiny, document oriented database optimized for your happiness."""

    homepage = "https://tinydb.readthedocs.io"
    pypi = "tinydb/tinydb-4.7.0.tar.gz"

    license("MIT")

    version(
        "4.7.1",
        sha256="1534e498ca23f55c43b0f1e7c0cf174049498ab45a887c82ba9831e0f9868df3",
        url="https://pypi.org/packages/0a/a9/303de29f4b293b5948c8c73f9ef92480329a4d37f6ba168c76250ab4c6b3/tinydb-4.7.1-py3-none-any.whl",
    )
    version(
        "4.7.0",
        sha256="e2cdf6e2dad49813e9b5fceb3c7943387309a8738125fbff0b58d248a033f7a9",
        url="https://pypi.org/packages/2c/76/93df2ac94dacc0f63e4263ee7cf4787d0c3df22859d9e0627958048f39c7/tinydb-4.7.0-py3-none-any.whl",
    )
    version(
        "4.6.1",
        sha256="ac1fdae2a7d5d7e2ca915d2666e685d63982991827c5dd097b6be4a3b5822dbc",
        url="https://pypi.org/packages/78/c0/60966b98a713b13a45f622607b57c08a83b9e491ff26a6595d47a442bac2/tinydb-4.6.1-py3-none-any.whl",
    )
    version(
        "4.6.0",
        sha256="9ecc1f2a0dc95aa00beeaf05b6ad3fa2884276eca6aea4f0850985689cc7076c",
        url="https://pypi.org/packages/a7/57/e2c128cc3e2b778ad92a5ebcdb1c63807113eea883cae219c76b6b191b38/tinydb-4.6.0-py3-none-any.whl",
    )
    version(
        "4.5.2",
        sha256="3c5e5c72c98db07e707be4e25f9e135a8a14b96938e4745b1b7187fec523ff58",
        url="https://pypi.org/packages/c7/a3/130a1949dfcf79915f2fe807947eeb91663d4a0bf8f7f2c0cc8d02d24620/tinydb-4.5.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:3", when="@4.7.1:")
        depends_on("python@:3", when="@4:4.7.0")
        depends_on("py-typing-extensions@3.10:", when="@4.6: ^python@:3.6")
        depends_on("py-typing-extensions@3.10:3", when="@4.5 ^python@:3.6")
