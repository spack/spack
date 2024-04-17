# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtDatalakeAnalytics(PythonPackage):
    """Microsoft Azure Data Lake Analytics Management Client Library for
    Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-datalake-analytics/azure-mgmt-datalake-analytics-0.6.0.zip"

    version(
        "0.6.0",
        sha256="ac96c9777314831db37461f0602e75298bc25277ba7f4d0d3e7966a926669b7e",
        url="https://pypi.org/packages/73/e7/5d909ef5812fc31f2871f3510ef43af93157ba51be03b6f798afba7a29d8/azure_mgmt_datalake_analytics-0.6.0-py2.py3-none-any.whl",
    )
    version(
        "0.2.1",
        sha256="4d02630f495c4b269d9512a9b214fa17c2400200cca1bdc5bcbc9dd9832956d8",
        url="https://pypi.org/packages/b0/b9/4aafa00ce427d72f2da84c942ea5f2d0c636f5b1b94eee269bac3d498c13/azure_mgmt_datalake_analytics-0.2.1-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common@1.1:", when="@0.2.1:")
        depends_on("py-azure-mgmt-datalake-nspkg@2:", when="@0.1.4:0")
        depends_on("py-msrestazure@0.4.27:", when="@0.5:0")
        depends_on("py-msrestazure@0.4.7:", when="@0.2.1:0.2")
