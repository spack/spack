# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureStorageCommon(PythonPackage):
    """Microsoft Azure Storage Common Client Library for Python."""

    homepage = "https://github.com/Azure/azure-storage-python"
    pypi = "azure-storage-common/azure-storage-common-2.1.0.tar.gz"

    license("MIT")

    version(
        "2.1.0",
        sha256="b01a491a18839b9d05a4fe3421458a0ddb5ab9443c14e487f40d16f9a1dc2fbe",
        url="https://pypi.org/packages/6b/a0/6794b318ce0118d1a4053bdf0149a60807407db9b710354f2b203c2f5975/azure_storage_common-2.1.0-py2.py3-none-any.whl",
    )
    version(
        "1.4.2",
        sha256="de4817cce35a23d1c89563edc38b481ebd8da4655bdf32d26fa2b06095179e4a",
        url="https://pypi.org/packages/05/6c/b2285bf3687768dbf61b6bc085b0c1be2893b6e2757a9d023263764177f3/azure_storage_common-1.4.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1.5:", when="@0.37.1:1.1,1.3,1.4.2:1,2.1:")
        depends_on("py-cryptography", when="@0.37.1:1.1,1.3,1.4.2:1,2.1:")
        depends_on("py-python-dateutil", when="@0.37.1:1.1,1.3,1.4.2:1,2.1:")
        depends_on("py-requests", when="@0.37.1:1.1,1.3,1.4.2:1,2.1:")
