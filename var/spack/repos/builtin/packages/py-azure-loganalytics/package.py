# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureLoganalytics(PythonPackage):
    """Microsoft Azure Log Analytics Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-loganalytics/azure-loganalytics-0.1.0.zip"

    version(
        "0.1.0",
        sha256="5a1bdb33e1fd3dfb275d9eec45ed8e1126eda51e9072ccf08a19922ee5e0ad98",
        url="https://pypi.org/packages/54/e2/1d30270441a50efce1d52eb426710fc98269eb8bdac44ee966bbd07846da/azure_loganalytics-0.1.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-azure-nspkg@2:", when="@:0.1.0")
        depends_on("py-msrest@0.4.29:", when="@:0.1.0")
