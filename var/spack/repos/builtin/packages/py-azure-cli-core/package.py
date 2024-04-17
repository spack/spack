# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureCliCore(PythonPackage):
    """Microsoft Azure Command-Line Tools Core Module."""

    homepage = "https://github.com/Azure/azure-cli"
    pypi = "azure-cli-core/azure-cli-core-2.9.1.tar.gz"

    license("MIT")

    version(
        "2.9.1",
        sha256="28bad5b4a8d90e98af4b556cbe560517a9be7187b0ea05bebe449c6838a03756",
        url="https://pypi.org/packages/cd/31/8801d6d4e96472e7d13eaf13227be57e1be78b3734ebbb4a79b832c9a8cd/azure_cli_core-2.9.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-adal@1.2.3:", when="@2.6:2.19")
        depends_on("py-argcomplete@1.8:1", when="@:2.43")
        depends_on("py-azure-cli-nspkg@2:", when="@:2.10")
        depends_on("py-azure-cli-telemetry", when="@:2.11")
        depends_on("py-azure-mgmt-core@1.0.0:1.0", when="@2.4:2.10")
        depends_on("py-azure-mgmt-resource@10:10.0", when="@2.8:2.9")
        depends_on("py-colorama@0.4.1:", when="@2.6:2.22")
        depends_on("py-humanfriendly@4.7:8", when="@2.3:2.17")
        depends_on("py-jmespath")
        depends_on("py-knack@0.7.1", when="@2.6:2.9")
        depends_on("py-msal@1:1.0", when="@2.5:2.19")
        depends_on("py-msal-extensions@0.1.3:0.1", when="@2.5:2.19")
        depends_on("py-msrest@0.4.4:", when="@:2.15")
        depends_on("py-msrestazure@0.6.3:", when="@2.4:2.24")
        depends_on("py-paramiko@2.0.8:2", when="@:2.45")
        depends_on("py-pkginfo@1.5.0.1:", when="@2.5:")
        depends_on("py-pyjwt", when="@:2.18")
        depends_on("py-pyopenssl@17.1:")
        depends_on("py-requests@2.22:", when="@2.6:2.25")
        depends_on("py-six@1.12:", when="@:2.29")
