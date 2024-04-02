# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNestAsyncio(PythonPackage):
    """Patch asyncio to allow nested event loops."""

    homepage = "https://github.com/erdewit/nest_asyncio"
    pypi = "nest-asyncio/nest_asyncio-1.4.0.tar.gz"

    license("BSD-2-Clause")

    version(
        "1.5.6",
        sha256="b9a953fb40dceaa587d109609098db21900182b16440652454a146cffb06e8b8",
        url="https://pypi.org/packages/e9/1a/6dd9ec31cfdb34cef8fea0055b593ee779a6f63c8e8038ad90d71b7f53c0/nest_asyncio-1.5.6-py3-none-any.whl",
    )
    version(
        "1.5.5",
        sha256="b98e3ec1b246135e4642eceffa5a6c23a3ab12c82ff816a92c612d68205813b2",
        url="https://pypi.org/packages/be/1e/a83058de46b40a392bdefcaac44d1d42db4bf8562cb68c95d6bae4b93276/nest_asyncio-1.5.5-py3-none-any.whl",
    )
    version(
        "1.5.4",
        sha256="3fdd0d6061a2bb16f21fe8a9c6a7945be83521d81a0d15cff52e9edee50101d6",
        url="https://pypi.org/packages/06/e0/93453ebab12f5ce9a9ceda2ff71648b30e5f2ce5bba19ee3c95cbd0aaa67/nest_asyncio-1.5.4-py3-none-any.whl",
    )
    version(
        "1.5.1",
        sha256="76d6e972265063fe92a90b9cc4fb82616e07d586b346ed9d2c89a4187acea39c",
        url="https://pypi.org/packages/52/e2/9b37da54e6e9094d2f558ae643d1954a0fa8215dfee4fa261f31c5439796/nest_asyncio-1.5.1-py3-none-any.whl",
    )
    version(
        "1.4.0",
        sha256="ea51120725212ef02e5870dd77fc67ba7343fc945e3b9a7ff93384436e043b6a",
        url="https://pypi.org/packages/a0/44/f2983c5be9803b08f89380229997e92c4bdd7a4a510ccee565b599d1bdc8/nest_asyncio-1.4.0-py3-none-any.whl",
    )
