# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtAppconfiguration(PythonPackage):
    """Microsoft Azure App Configuration Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-appconfiguration/azure-mgmt-appconfiguration-0.5.0.zip"

    version(
        "0.5.0",
        sha256="9d7e2ceebc09c8b2b46173712032590769f61ddffc94b9e27fe418345a3e433c",
        url="https://pypi.org/packages/be/5d/4fb60b2d6a0aac3bc39df7aa97a98c3e28b7274307461b75e2f594613ed6/azure_mgmt_appconfiguration-0.5.0-py2.py3-none-any.whl",
    )
    version(
        "0.4.0",
        sha256="85b9fdf879d939a14ddb480d5ae5552439da8daf6766f0ba6b2c4218b3fc2c78",
        url="https://pypi.org/packages/ce/54/5a7379aa323d9c2dfc0438fe30d5def41c66cf6cd7e7a0ab656dbd396fab/azure_mgmt_appconfiguration-0.4.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@:1")
        depends_on("py-msrestazure@0.4.32:", when="@:0")
