# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtAuthorization(PythonPackage):
    """Microsoft Azure Authorization Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-authorization/azure-mgmt-authorization-0.60.0.zip"

    version(
        "0.60.0",
        sha256="9d64295cf4210ec14e98fb024a6b4d79d68ef50cdb3804f0b53f8567e52d847f",
        url="https://pypi.org/packages/5e/17/4724694ddb3311955ddc367eddcd0928f8ee2c7b12d5a6f0b12bca0b03db/azure_mgmt_authorization-0.60.0-py2.py3-none-any.whl",
    )
    version(
        "0.52.0",
        sha256="2152f345840d6948e41cd259e44e70dd08186f3ce42fbc1816f99a93145ed0a4",
        url="https://pypi.org/packages/6b/b2/c0d62a3a91c13641e09af294c13fe16929f88dc5902718388cd9b292217f/azure_mgmt_authorization-0.52.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common@1.1:", when="@0.40,0.51:")
        depends_on("py-msrest@0.5:", when="@0.51:1")
        depends_on("py-msrestazure@0.4.32:", when="@0.51:0")
