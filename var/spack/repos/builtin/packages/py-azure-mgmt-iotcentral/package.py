# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtIotcentral(PythonPackage):
    """Microsoft Azure IoTCentral Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-iotcentral/azure-mgmt-iotcentral-3.1.0.zip"

    version(
        "3.1.0",
        sha256="4d2966071af4aaee9f93707d71eb6e66259ef5546aea66f2ac5c455c23b0103a",
        url="https://pypi.org/packages/93/78/ed0f333b5b4a2fbedea600056084674debd2f89869f2a212dddee6599ed2/azure_mgmt_iotcentral-3.1.0-py2.py3-none-any.whl",
    )
    version(
        "3.0.0",
        sha256="81c7b612da2c5de505338ec0091fc6acf1a26560d1bc3127e5de72fcbed8356f",
        url="https://pypi.org/packages/56/15/f17e6b6b1e9c5808a3a1d0817241e5cfa8c8f4adec081568fe7c863e5038/azure_mgmt_iotcentral-3.0.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@0.2:4")
        depends_on("py-msrestazure@0.4.32:", when="@0.2:4")
