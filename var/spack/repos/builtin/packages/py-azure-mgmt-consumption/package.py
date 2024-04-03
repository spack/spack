# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtConsumption(PythonPackage):
    """Microsoft Azure Consumption Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-consumption/azure-mgmt-consumption-3.0.0.zip"

    version(
        "3.0.0",
        sha256="af319ad6e3ec162a7578563f149e3cdd7d833a62ec80761cfd93caf79467610b",
        url="https://pypi.org/packages/3f/97/c13a39c275b2cae19041b1ed36b7f7e53fbeb02c44f6a30235e867306ff1/azure_mgmt_consumption-3.0.0-py2.py3-none-any.whl",
    )
    version(
        "2.0.0",
        sha256="36ea28bb2ed4bec7e4d643444085ba4debed20a01fbd87f599896a4bda3318bd",
        url="https://pypi.org/packages/11/f4/2db9557494dfb17ff3edeae5726981143a7baace17df3712b189e343bd8c/azure_mgmt_consumption-2.0.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:", when="@1.1:")
        depends_on("py-azure-mgmt-nspkg@2:", when="@:2")
        depends_on("py-msrest@0.5:", when="@3:8")
        depends_on("py-msrestazure@0.4.32:", when="@3")
        depends_on("py-msrestazure@0.4.20:", when="@2")
