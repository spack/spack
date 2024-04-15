# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtRdbms(PythonPackage):
    """Microsoft Azure RDBMS Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-rdbms/azure-mgmt-rdbms-2.2.0.zip"

    version(
        "2.2.0",
        sha256="d05afdc929dfb586caf60958d86428d9445e43661a7abc0cc95f47dc31828fe9",
        url="https://pypi.org/packages/63/91/1085293d9a28f707d3c8a5c6676114be0bb0cfea5e78226d1f7a02df6843/azure_mgmt_rdbms-2.2.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-common@1.1:")
        depends_on("py-msrest@0.5:", when="@:8.1.0-beta2")
        depends_on("py-msrestazure@0.4.32:", when="@:3")
