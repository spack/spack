# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtResource(PythonPackage):
    """Microsoft Azure Resource Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-resource/azure-mgmt-resource-10.0.0.zip"

    version(
        "10.0.0",
        sha256="c1e2d834dee84953a4e25bef119008854a861d6d3fbe79b436589dc042e5a7c5",
        url="https://pypi.org/packages/be/20/b639d8e4b0c1c49e3f1373c6a7948fd4ced55e57f204b63fb15a7cd77e73/azure_mgmt_resource-10.0.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@:16.0")
        depends_on("py-msrestazure@0.4.32:", when="@:13")
