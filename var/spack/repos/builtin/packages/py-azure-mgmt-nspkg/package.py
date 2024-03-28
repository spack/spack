# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtNspkg(PythonPackage):
    """Microsoft Azure Resource Management Namespace Package [Internal]."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-nspkg/azure-mgmt-nspkg-3.0.2.zip"

    version(
        "3.0.2",
        sha256="1c6f5134de78c8907e8b73a8ceaaf1f336a24193a543039994fe002bb5f7f39f",
        url="https://pypi.org/packages/a1/6e/464d039ec6184234b188d6a9d199e658cce86b38afe4db0e8edd1629f3f6/azure_mgmt_nspkg-3.0.2-py2-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-nspkg@3:", when="@3:")
