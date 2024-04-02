# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtContainerregistry(PythonPackage):
    """Microsoft Azure Container Registry Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-containerregistry/azure-mgmt-containerregistry-2.8.0.zip"

    # Release candidate needed for py-azure-cli
    version(
        "3.0.0-rc14",
        sha256="bac9a280b7c25a0a2acb0e8a00500ebfcaf9c580a2f2a3302b77ab2f4b09261e",
        url="https://pypi.org/packages/7e/ba/c61d1194088d88de079ae0d02529229dc15c2f84d43c6b7f6c3ed06fa39d/azure_mgmt_containerregistry-3.0.0rc14-py2.py3-none-any.whl",
    )
    version(
        "2.8.0",
        sha256="7de7c542e29b441f3858447694c4e5ab933eeef74bce2dd5bdab32b6d521ecd3",
        url="https://pypi.org/packages/97/70/8c2d0509db466678eba16fa2b0a539499f3b351b1f2993126ad843d5be13/azure_mgmt_containerregistry-2.8.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:", when="@:1,2.2:")
        depends_on("py-msrest@0.5:", when="@2.1:8.0.0-beta1")
        depends_on("py-msrestazure@0.4.32:", when="@2.1:3")
