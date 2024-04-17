# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtManagementgroups(PythonPackage):
    """Microsoft Azure Management Groups Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-managementgroups/azure-mgmt-managementgroups-0.2.0.zip"

    version(
        "0.2.0",
        sha256="8194ee6274df865eccd1ed9d385ea625aeba9b8058b9e4fdf547f5207271a775",
        url="https://pypi.org/packages/95/e8/2bbe79c62ad2787944dd7ae4d06d60afb3967b5efc09ed14046919371b59/azure_mgmt_managementgroups-0.2.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@0.2:1.0.0-beta1")
        depends_on("py-msrestazure@0.4.32:", when="@0.2:0")
