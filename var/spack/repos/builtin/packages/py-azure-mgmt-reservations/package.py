# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtReservations(PythonPackage):
    """Microsoft Azure Reservations Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-reservations/azure-mgmt-reservations-0.7.0.zip"

    version(
        "0.7.0",
        sha256="0eccdb5c3284500f470ad85de65784424211049355c31316c3a39777c697470a",
        url="https://pypi.org/packages/7a/d6/07fb34b612efccdb5e7ebbe0d84f7ae3a48bb54a920e664376fc31b8a0fd/azure_mgmt_reservations-0.7.0-py2.py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="e592ebf163f9641fc4367202b470ee7c85ba221a3b979a0045c693002cc2eb59",
        url="https://pypi.org/packages/6a/88/0d5f230fab1a72e22f22defba9b2d11241ae229b179617950b1473a1d06f/azure_mgmt_reservations-0.6.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@0.3:1.0.0-beta1")
        depends_on("py-msrestazure@0.4.32:", when="@0.3:0")
