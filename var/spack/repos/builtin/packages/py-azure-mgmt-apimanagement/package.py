# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtApimanagement(PythonPackage):
    """Microsoft Azure API Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-apimanagement/azure-mgmt-apimanagement-0.2.0.zip"

    version(
        "0.2.0",
        sha256="815c98f7fb6a3429caea496cb6637b58ee005e710b5f825c8e980318586cc338",
        url="https://pypi.org/packages/95/4e/0884a860dff4bf16760ec5ed248e6a2a9b9457502fe525ebdeed773c31bf/azure_mgmt_apimanagement-0.2.0-py2.py3-none-any.whl",
    )
    version(
        "0.1.0",
        sha256="71007d356618d421c208a365f85f334cf21819bd439dbbf4ff252202da74f219",
        url="https://pypi.org/packages/af/50/6c514ad0850dbd371bdce481661cd4bbd61e569cc44478adf4dc92eeac3c/azure_mgmt_apimanagement-0.1.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:", when="@:4.0.0")
        depends_on("py-msrest@0.5:", when="@:2.0")
        depends_on("py-msrestazure@0.4.32:", when="@:0")
