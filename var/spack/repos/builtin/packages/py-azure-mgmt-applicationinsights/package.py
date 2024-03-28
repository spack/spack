# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtApplicationinsights(PythonPackage):
    """Microsoft Azure Application Insights Management Client Library for
    Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-applicationinsights/azure-mgmt-applicationinsights-0.3.0.zip"

    version(
        "0.3.0",
        sha256="d4d9e8d4d425e64c2ba029eaee85161167c5305dbf5320400152885be73abdad",
        url="https://pypi.org/packages/04/46/b8d72767576bfc2f4370d8c1395295accca0f14b8cc0f327987fb23b513d/azure_mgmt_applicationinsights-0.3.0-py2.py3-none-any.whl",
    )
    version(
        "0.1.1",
        sha256="929c30559692c77d424ca36f11e98f066c98e7eb7b742c44beadc082715f19df",
        url="https://pypi.org/packages/30/61/1d95a5ef3a9119a0d375d8670129375515de20e20409612e9671c99bd19f/azure_mgmt_applicationinsights-0.1.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-azure-mgmt-nspkg@2:", when="@:0.1")
        depends_on("py-msrest@0.5:", when="@0.2:1")
        depends_on("py-msrestazure@0.4.32:", when="@0.2:0")
        depends_on("py-msrestazure@0.4.20:", when="@:0.1")
