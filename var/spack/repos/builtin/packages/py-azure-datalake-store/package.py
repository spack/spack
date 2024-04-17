# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureDatalakeStore(PythonPackage):
    """Azure Data Lake Store Filesystem Client Library for Python."""

    homepage = "https://github.com/Azure/azure-data-lake-store-python"
    pypi = "azure-datalake-store/azure-datalake-store-0.0.48.tar.gz"

    version(
        "0.0.48",
        sha256="b35108939f9ac4b6bc568e9b735e3e38a5fdabe00065073b5e48659929d536d1",
        url="https://pypi.org/packages/27/9a/e7140775b3f8f011ef5d001c12a3519310094375671950105519e30bb12b/azure_datalake_store-0.0.48-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-adal@0.4.2:", when="@:0.0.52")
        depends_on("py-cffi")
        depends_on("py-requests@2.20:")
