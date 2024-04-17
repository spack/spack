# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtKusto(PythonPackage):
    """Microsoft Azure Kusto Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-kusto/azure-mgmt-kusto-0.9.0.zip"

    version(
        "0.9.0",
        sha256="4bc854108d64372a0b21d948338ea1d25742df6816d2393554b8efdd00028916",
        url="https://pypi.org/packages/65/7a/2e9d629252c5667cf5fad0d70502ac2d2bee061bf0001295821ae40740ef/azure_mgmt_kusto-0.9.0-py2.py3-none-any.whl",
    )
    version(
        "0.3.0",
        sha256="57a6a1a9fd0be60e5d5ff7d00bae4e9dd645308dab277b6712786aae22b5e435",
        url="https://pypi.org/packages/d9/4f/4ef96c0bb0fec6eb7d0786a01f8f41851f10b0b26334992ba7e2b8a12c19/azure_mgmt_kusto-0.3.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@:1")
        depends_on("py-msrestazure@0.4.32:", when="@:0")
