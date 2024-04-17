# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtContainerservice(PythonPackage):
    """Microsoft Azure Container Service Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-containerservice/azure-mgmt-containerservice-9.2.0.zip"

    version(
        "9.2.0",
        sha256="48f8668e44d57b5051e4600892eedca8a7d5ad1e6d97c04814ccf0f84c2a929e",
        url="https://pypi.org/packages/81/4f/66efb520f393950fe481dee7ec3e6c56031248429742ea156c7a4f52e409/azure_mgmt_containerservice-9.2.0-py2.py3-none-any.whl",
    )
    version(
        "9.0.1",
        sha256="401ebff271865ad00b10474732aea3cfbc5edbed7d9caa8b3e28cd8835bb3534",
        url="https://pypi.org/packages/f2/ae/e44af67874fcc45530c01511939fa301ca90096f92bf70b21631883f6fff/azure_mgmt_containerservice-9.0.1-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@:15.0")
        depends_on("py-msrestazure@0.4.32:", when="@:12")
