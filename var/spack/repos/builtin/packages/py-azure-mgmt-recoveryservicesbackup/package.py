# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtRecoveryservicesbackup(PythonPackage):
    """Microsoft Azure Recovery Services Backup Management Client Library for
    Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-recoveryservicesbackup/azure-mgmt-recoveryservicesbackup-0.8.0.zip"

    version(
        "0.8.0",
        sha256="ddeb71c8cf1af28915e82c92fb16a3a494ca28f5bb1cc0ffa68511f0ccc40a80",
        url="https://pypi.org/packages/14/3c/637ee8a2b5b5051f54c3d9a3a5266b1d1215300c45f09d6c4848b4bff18b/azure_mgmt_recoveryservicesbackup-0.8.0-py2.py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="5668608ac210af2feac8baddf5ce4d27d048330841743a95977c7962e338b94e",
        url="https://pypi.org/packages/db/5d/4e4894a019be8db422fe27179e3b5f7f9751cd2d7f7025b03a8e723fced2/azure_mgmt_recoveryservicesbackup-0.6.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:", when="@0.1.1:")
        depends_on("py-msrest@0.5:", when="@0.4:0")
        depends_on("py-msrestazure@0.4.32:", when="@0.4:0")
