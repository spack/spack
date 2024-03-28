# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtTrafficmanager(PythonPackage):
    """Microsoft Azure Traffic Manager Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-trafficmanager/azure-mgmt-trafficmanager-0.51.0.zip"

    version(
        "0.51.0",
        sha256="672f909459e70d41eb8d7bc619839cd60eb2cea2fd20dc7924b7e9670ea8aedf",
        url="https://pypi.org/packages/b1/2d/2a95dd8e57fa0c96548f0c1b11936c9820a40344e39660e3aebd63796c26/azure_mgmt_trafficmanager-0.51.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:", when="@0.50:")
        depends_on("py-msrest@0.5:", when="@0.51:0")
        depends_on("py-msrestazure@0.4.32:", when="@0.51:0")
