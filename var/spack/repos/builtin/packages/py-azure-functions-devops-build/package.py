# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureFunctionsDevopsBuild(PythonPackage):
    """Python package for integrating Azure Functions with Azure DevOps.
    Specifically made for the Azure CLI."""

    homepage = "https://github.com/Azure/azure-functions-devops-build"
    pypi = "azure-functions-devops-build/azure-functions-devops-build-0.0.22.tar.gz"

    license("MIT")

    version(
        "0.0.22",
        sha256="adc4c45de5510acf4c094df84b54bc7767e1466e4bfdce23b99ffccf29de3f2f",
        url="https://pypi.org/packages/96/57/65ca02568edf21abbb0831dedb3f87b6c2164bd4188778865f27b8a05645/azure_functions_devops_build-0.0.22-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-jinja2", when="@0.0.18:")
        depends_on("py-msrest", when="@0.0.18:")
        depends_on("py-vsts", when="@0.0.18:")
