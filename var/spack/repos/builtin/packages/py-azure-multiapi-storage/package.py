# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMultiapiStorage(PythonPackage):
    """Microsoft Azure Storage Client Library for Python with multi API
    version support."""

    homepage = "https://github.com/Azure/azure-multiapi-storage-python"
    pypi = "azure-multiapi-storage/azure-multiapi-storage-0.3.5.tar.gz"

    license("MIT")

    version(
        "0.3.5",
        sha256="d31340b073f20b55f1a3736e390b4dc227061ba7d99af8a84584e8b3a724ff49",
        url="https://pypi.org/packages/e6/a9/79b98b5d27b407dd6bae32c453f3151819becd74c27e2bcdf7e6fb3806e7/azure_multiapi_storage-0.3.5-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common")
        depends_on("py-azure-core", when="@0.3:0.5")
        depends_on("py-cryptography", when="@:0.5")
        depends_on("py-python-dateutil")
        depends_on("py-requests")
