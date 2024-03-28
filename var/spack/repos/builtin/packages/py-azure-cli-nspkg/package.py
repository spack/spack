# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureCliNspkg(PythonPackage):
    """Microsoft Azure CLI Namespace Package."""

    homepage = "https://github.com/Azure/azure-cli"
    pypi = "azure-cli-nspkg/azure-cli-nspkg-3.0.4.tar.gz"

    license("MIT")

    version(
        "3.0.4",
        sha256="34ff69dfed9180aa945bca2c0b7e5603d84e92b28c531efe4beae51a7230791d",
        url="https://pypi.org/packages/fe/1f/babf85745bc6b1ab770e38a330edd651dde61dd662174adb562d4452d9be/azure_cli_nspkg-3.0.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-nspkg@2:", when="@3:3.0.0,3.0.2:")
