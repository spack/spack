# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureCliTelemetry(PythonPackage):
    """Microsoft Azure CLI Telemetry Package."""

    homepage = "https://github.com/Azure/azure-cli"
    pypi = "azure-cli-telemetry/azure-cli-telemetry-1.0.4.tar.gz"

    license("MIT")

    version(
        "1.0.4",
        sha256="421e80c2fe3fdff8c38d27ee1fdfdfef1326c79212d6e23a6ebe308d19df552a",
        url="https://pypi.org/packages/f9/eb/4137d6cf4c91c135260dbf566b5fc8fc6d427b3f807523e388dc030dcc65/azure_cli_telemetry-1.0.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-applicationinsights@0.11.1:", when="@1.0.3:")
        depends_on("py-azure-cli-nspkg@2:", when="@:1.0.4")
        depends_on("py-portalocker@1.2:1", when="@1.0.3:1.0.6")
