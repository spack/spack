# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtEventhub(PythonPackage):
    """Microsoft Azure EventHub Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-eventhub/azure-mgmt-eventhub-4.0.0.zip"

    version(
        "4.0.0",
        sha256="73473ca48a184365508b1c0e9d2dcb5efd315b9cbb3ead666f5135c65f2afbd4",
        url="https://pypi.org/packages/e0/06/a467f90fbecce2b4042e982e40faba0c32106b6b364909d17b0f6e5e5611/azure_mgmt_eventhub-4.0.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@2.1:8")
        depends_on("py-msrestazure@0.4.32:", when="@2.1:5")
