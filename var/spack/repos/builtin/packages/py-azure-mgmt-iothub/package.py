# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtIothub(PythonPackage):
    """Microsoft Azure IoTHub Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-iothub/azure-mgmt-iothub-0.12.0.zip"

    version(
        "0.12.0",
        sha256="adc411b57b61e12d2b05f3479404b703d6719c6ebe60932a3aba3cde4e917715",
        url="https://pypi.org/packages/df/39/bace873ec0a4e9dec0e2467e18ddb67c46f425d4de1ff88c35f38314de71/azure_mgmt_iothub-0.12.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@0.6:1")
        depends_on("py-msrestazure@0.4.32:", when="@0.6:0")
