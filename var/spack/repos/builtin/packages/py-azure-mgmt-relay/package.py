# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtRelay(PythonPackage):
    """Microsoft Azure Relay Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-relay/azure-mgmt-relay-0.2.0.zip"

    version(
        "0.2.0",
        sha256="dd73eb46116efa116306d2fbd9b6db555791e683c84cae13b4972ea5d81a7da1",
        url="https://pypi.org/packages/75/1c/686277342859a1882eecac7d801dc84deb21eb22182db4e19c25c2bd5c67/azure_mgmt_relay-0.2.0-py2.py3-none-any.whl",
    )
    version(
        "0.1.0",
        sha256="1411e734573ce6166ac7a75fbfc0afb7d6b3f47a94d0b4999b6adf2709eba87c",
        url="https://pypi.org/packages/00/f7/f5c72bd19829cfaf9f070ec294c901ad7f98835ba9560fdad652afb1071f/azure_mgmt_relay-0.1.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-azure-mgmt-nspkg@2:", when="@:0.1")
        depends_on("py-msrest@0.5:", when="@0.2:1.0")
        depends_on("py-msrestazure@0.4.32:", when="@0.2:0")
        depends_on("py-msrestazure@0.4.20:", when="@:0.1")
