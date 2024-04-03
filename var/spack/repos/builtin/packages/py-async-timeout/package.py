# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAsyncTimeout(PythonPackage):
    """asyncio-compatible timeout context manager."""

    homepage = "https://github.com/aio-libs/async-timeout"
    pypi = "async-timeout/async-timeout-3.0.1.tar.gz"

    license("Apache-2.0")

    version(
        "4.0.2",
        sha256="8ca1e4fcf50d07413d66d1a5e416e42cfdf5851c981d679a09851a6853383b3c",
        url="https://pypi.org/packages/d6/c1/8991e7c5385b897b8c020cdaad718c5b087a6626d1d11a23e1ea87e325a7/async_timeout-4.0.2-py3-none-any.whl",
    )
    version(
        "4.0.1",
        sha256="a22c0b311af23337eb05fcf05a8b51c3ea53729d46fb5460af62bee033cec690",
        url="https://pypi.org/packages/41/4a/2ca8802045b6df8dd25a0f8f7c216808e9e3bff2809efe4a36cc99d35cca/async_timeout-4.0.1-py3-none-any.whl",
    )
    version(
        "4.0.0",
        sha256="f3303dddf6cafa748a92747ab6c2ecf60e0aeca769aee4c151adfce243a05d9b",
        url="https://pypi.org/packages/53/a9/cd484af830e5c525553da1a585ff4fe6f1d91a12f0131c736a3ef0d99cce/async_timeout-4.0.0-py3-none-any.whl",
    )
    version(
        "3.0.1",
        sha256="4291ca197d287d274d0b6cb5d6f8f8f82d434ed288f962539ff18cc9012f9ea3",
        url="https://pypi.org/packages/e1/1e/5a4441be21b0726c4464f3f23c8b19628372f606755a9d2e46c187e65ec4/async_timeout-3.0.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-typing-extensions@3.6.5:", when="@4.0.2: ^python@:3.7")
        depends_on("py-typing-extensions@3.6.5:", when="@4.0.0-alpha2:4.0.1")
