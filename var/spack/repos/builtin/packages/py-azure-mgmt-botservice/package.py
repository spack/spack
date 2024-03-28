# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtBotservice(PythonPackage):
    """Microsoft Azure Bot Service Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-botservice/azure-mgmt-botservice-0.2.0.zip"

    version(
        "0.2.0",
        sha256="375584c849ca4a21ff6d9b5621b69b249bbdb9470560dcd77820f8daf3ff2fb1",
        url="https://pypi.org/packages/93/36/c60c52101257bc30338993a38c1db0e33561e4361a1ba521f91476e845ab/azure_mgmt_botservice-0.2.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@:1.0.0-beta1")
        depends_on("py-msrestazure@0.4.32:", when="@:0")
