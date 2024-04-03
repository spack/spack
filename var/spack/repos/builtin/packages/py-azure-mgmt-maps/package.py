# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtMaps(PythonPackage):
    """Microsoft Azure Maps Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-maps/azure-mgmt-maps-0.1.0.zip"

    version(
        "0.1.0",
        sha256="a779b1ddbbcd95393e53f11b586dd26c42a709aaa226412a2df64d0da6807a80",
        url="https://pypi.org/packages/e4/04/c64326729e842f3eab1fd527f7582e269e4b0e5b9324a4562edaf0371953/azure_mgmt_maps-0.1.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:")
        depends_on("py-azure-mgmt-nspkg@2:", when="@:0.1")
        depends_on("py-msrestazure@0.4.27:", when="@:0.1")
