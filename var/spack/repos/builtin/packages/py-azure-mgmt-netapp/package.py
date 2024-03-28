# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtNetapp(PythonPackage):
    """Microsoft Azure NetApp Files Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-netapp/azure-mgmt-netapp-0.11.0.zip"

    version(
        "0.11.0",
        sha256="7c4ca42d2ce866f59ff00e1d4ac9e211920137d06bc904a1d6f895061c15bd95",
        url="https://pypi.org/packages/c8/57/c04cc191e0150c9988dd12be0ab649cb885c0eba1c1681576365d9f36016/azure_mgmt_netapp-0.11.0-py2.py3-none-any.whl",
    )
    version(
        "0.8.0",
        sha256="0ef7b3833a8eaca03c265f7b603535529a873220eca7514c32232a53873cb6d2",
        url="https://pypi.org/packages/37/8e/6ee8663a91d9188b60ccd38148d7d273d23b397d07228034fe4a31caa555/azure_mgmt_netapp-0.8.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@:2")
        depends_on("py-msrestazure@0.4.32:", when="@:0")
