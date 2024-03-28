# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAnyio(PythonPackage):
    """High level compatibility layer for multiple asynchronous event loop
    implementations."""

    homepage = "https://github.com/agronholm/anyio"
    pypi = "anyio/anyio-3.2.1.tar.gz"

    license("MIT")

    version(
        "4.0.0",
        sha256="cfdb2b588b9fc25ede96d8db56ed50848b0b649dca3dd1df0b11f683bb9e0b5f",
        url="https://pypi.org/packages/36/55/ad4de788d84a630656ece71059665e01ca793c04294c463fd84132f40fe6/anyio-4.0.0-py3-none-any.whl",
    )
    version(
        "3.6.2",
        sha256="fbbe32bd270d2a2ef3ed1c5d45041250284e31fc0a4df4a5a6071842051a51e3",
        url="https://pypi.org/packages/77/2b/b4c0b7a3f3d61adb1a1e0b78f90a94e2b6162a043880704b7437ef297cad/anyio-3.6.2-py3-none-any.whl",
    )
    version(
        "3.6.1",
        sha256="cb29b9c70620506a9a8f87a309591713446953302d7d995344d0d7c6c0c9a7be",
        url="https://pypi.org/packages/c3/22/4cba7e1b4f45ffbefd2ca817a6800ba1c671c26f288d7705f20289872012/anyio-3.6.1-py3-none-any.whl",
    )
    version(
        "3.5.0",
        sha256="b5fa16c5ff93fa1046f2eeb5bbff2dad4d3514d6cda61d02816dba34fa8c3c2e",
        url="https://pypi.org/packages/b1/ae/9a8af72d6f0c551943903eefcf93c3a29898fb7b594603c0d70679c199b1/anyio-3.5.0-py3-none-any.whl",
    )
    version(
        "3.3.4",
        sha256="4fd09a25ab7fa01d34512b7249e366cd10358cdafc95022c7ff8c8f8a5026d66",
        url="https://pypi.org/packages/e6/bc/832d33ddcf7bcfdfa73cd1780847726dee4581adac9d4ca975feb8e7662c/anyio-3.3.4-py3-none-any.whl",
    )
    version(
        "3.2.1",
        sha256="442678a3c7e1cdcdbc37dcfe4527aa851b1b0c9162653b516e9f509821691d50",
        url="https://pypi.org/packages/5a/8c/6712b0aebe9b250736ec5dde99883b143290b49ecc2310eb583577e316aa/anyio-3.2.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-exceptiongroup@1.0.2:", when="@4: ^python@:3.10")
        depends_on("py-idna@2.8:", when="@1.4:")
        depends_on("py-sniffio@1.1:", when="@1.0.0-rc2:")

    # Historical dependencies
