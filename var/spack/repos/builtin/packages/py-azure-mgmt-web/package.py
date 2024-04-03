# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtWeb(PythonPackage):
    """Microsoft Azure Web Apps Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-web/azure-mgmt-web-0.47.0.zip"

    version(
        "0.47.0",
        sha256="dd546f432444a155e9cb7487d77e00a581eecf4ad851ac48f35c8541dd33182f",
        url="https://pypi.org/packages/b6/76/b6b800d686f38b010d2b911bfb1ef820ff9659e884f2cf2470360546981e/azure_mgmt_web-0.47.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@0.40:2")
        depends_on("py-msrestazure@0.4.32:", when="@0.40:0")
