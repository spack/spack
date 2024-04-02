# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureCore(PythonPackage):
    """Microsoft Azure Core Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/core/azure-core"
    pypi = "azure-core/azure-core-1.30.0.tar.gz"

    license("MIT")

    version(
        "1.30.0",
        sha256="3dae7962aad109610e68c9a7abb31d79720e1d982ddf61363038d175a5025e89",
        url="https://pypi.org/packages/be/4f/a747b2537fea6302ff3a307b1f9701853e65e215afc1a62fa931d031c57a/azure_core-1.30.0-py3-none-any.whl",
    )
    version(
        "1.29.7",
        sha256="95a7b41b4af102e5fcdfac9500fcc82ff86e936c7145a099b7848b9ac0501250",
        url="https://pypi.org/packages/ff/29/dbc7182bc207530c7b5858d59f429158465f878845d64a038afc1aa61e35/azure_core-1.29.7-py3-none-any.whl",
    )
    version(
        "1.29.2",
        sha256="8e6602f322dc1070caf7e17754beb53b69ffa09df0f4786009a3107e9a00c793",
        url="https://pypi.org/packages/78/f5/0e2e1eee5548ef539461183024ccdd0397a920b33fdd092c9af489ab1940/azure_core-1.29.2-py3-none-any.whl",
    )
    version(
        "1.28.0",
        sha256="dec36dfc8eb0b052a853f30c07437effec2f9e3e1fc8f703d9bdaa5cfc0043d9",
        url="https://pypi.org/packages/c3/0a/32b17d776a6bf5ddaa9dbad0e88de9d28a55bec1d37b8d408cc7d2e5e28d/azure_core-1.28.0-py3-none-any.whl",
    )
    version(
        "1.27.1",
        sha256="1b4b19f455eb7b4332c6f92adc2c669353ded07c2722eb436165f0c253737792",
        url="https://pypi.org/packages/71/fa/b6f8f8693de85c69f70ad3b0320a35b663ef1110d32ee2c1064d3dacb0f4/azure_core-1.27.1-py3-none-any.whl",
    )
    version(
        "1.26.4",
        sha256="d9664b4bc2675d72fba461a285ac43ae33abb2967014a955bf136d9703a2ab3c",
        url="https://pypi.org/packages/8d/12/8d1b124dcce9a695a8a8907461684ad08af4eca575e59fb2c8c70539caf7/azure_core-1.26.4-py3-none-any.whl",
    )
    version(
        "1.26.1",
        sha256="726ffd1ded04a2c1cb53f9d9155cbb05ac5c1c2a29af4ef622e93e1c0a8bc92b",
        url="https://pypi.org/packages/2c/e9/a58441e746621541bf122ed820f756dcfb8ede7b863b5f8e301236cf1e2f/azure_core-1.26.1-py3-none-any.whl",
    )
    version(
        "1.21.1",
        sha256="3d70e9ec64de92dfae330c15bc69085caceb2d83813ef6c01cc45326f2a4be83",
        url="https://pypi.org/packages/a6/07/95105c0c1cc46a5c8b14e43c66fa8b50fe1e7f0918e8809a7422cb67a1cf/azure_core-1.21.1-py2.py3-none-any.whl",
    )
    version(
        "1.7.0",
        sha256="2d1aade2795ea0ac2a903af940c3e0dfe75d25351ec4fc44edf747e97d703dfb",
        url="https://pypi.org/packages/8b/00/efb68e2dda82139d732090fc3b7ff47fe6f34724ea7ba31e518a854b15c1/azure_core-1.7.0-py2.py3-none-any.whl",
    )
    version(
        "1.6.0",
        sha256="7bf695b017acea3da28e0390a2dea5b7e15a9fa3ef1af50ff020bcfe7dacb6a4",
        url="https://pypi.org/packages/a4/ed/ff9f4669e5b9a78a62fe43b83cc01e9007bbf6e99ec7ab6f73557135099f/azure_core-1.6.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@1.25:")
        depends_on("py-requests@2.21:", when="@1.29.6:")
        depends_on("py-requests@2.18.4:", when="@:1.29.5")
        depends_on("py-six@1.11:", when="@1.11:")
        depends_on("py-six@1.6:", when="@:1.10")
        depends_on("py-typing-extensions@4.6:", when="@1.29.2:")
        depends_on("py-typing-extensions@4.3:", when="@1.26.4:1.29.1")
        depends_on("py-typing-extensions@4.0.1:", when="@1.23:1.26.3")

    # https://github.com/Azure/azure-sdk-for-python/blob/azure-core_1.30.0/sdk/core/azure-core/setup.py
