# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtPrivatedns(PythonPackage):
    """Microsoft Azure DNS Private Zones Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-privatedns/azure-mgmt-privatedns-0.1.0.zip"

    version(
        "0.1.0",
        sha256="aeea39403333b280ceb7086cda6ea98ba78472735c1a14388e16d22ea87974c7",
        url="https://pypi.org/packages/f1/47/fd5dba6d5f57c97bf21b4bf9e13bef73b50cab0b18bc171e497057f7e474/azure_mgmt_privatedns-0.1.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@:1.0")
        depends_on("py-msrestazure@0.4.32:", when="@:0")
