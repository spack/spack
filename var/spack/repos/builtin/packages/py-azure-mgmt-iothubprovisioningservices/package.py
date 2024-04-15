# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtIothubprovisioningservices(PythonPackage):
    """Microsoft Azure IoTHub Provisioning Services Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-iothubprovisioningservices/azure-mgmt-iothubprovisioningservices-0.2.0.zip"

    version(
        "0.2.0",
        sha256="2b3480a8ad2e535928da55de92b6127d02171768fed375b112274eb1e55268c1",
        url="https://pypi.org/packages/84/ce/3500c731a5c5b31028e662aa41bc45f75301834a0c03adeacfe7ef7bd86e/azure_mgmt_iothubprovisioningservices-0.2.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common@1.1:")
        depends_on("py-azure-mgmt-nspkg@2:", when="@:0.2")
        depends_on("py-msrestazure@0.4.20:", when="@0.2")
