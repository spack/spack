# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtServicebus(PythonPackage):
    """Microsoft Azure Service Bus Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-servicebus/azure-mgmt-servicebus-0.6.0.zip"

    version(
        "0.6.0",
        sha256="bfa726ffd5ba99ef4985dd8bcc6f8f1ff42a321ad67811914be23e92631a4c5f",
        url="https://pypi.org/packages/1e/8c/3e9479ed7344223399d3cf58aaea0679390a5dada659df41dbf32bc77f37/azure_mgmt_servicebus-0.6.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common@1.1:", when="@0.3.1:")
        depends_on("py-msrest@0.5:", when="@0.5.2:6")
        depends_on("py-msrestazure@0.4.32:", when="@0.5.2:2")
