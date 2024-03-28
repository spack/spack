# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtCognitiveservices(PythonPackage):
    """Microsoft Azure Cognitive Services Management Client Library for
    Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-cognitiveservices/azure-mgmt-cognitiveservices-6.2.0.zip"

    version(
        "6.2.0",
        sha256="6b17d4e13964cdce86bf48e893c9171b374b11e5bba65fb4928ad434256a4f37",
        url="https://pypi.org/packages/68/e3/2470cc6d53640914e7dcea754fbb714a784c37cb50f309bebcca3b8217cb/azure_mgmt_cognitiveservices-6.2.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-azure-common@1.1:", when="@2:")
        depends_on("py-msrest@0.5:", when="@4:11")
        depends_on("py-msrestazure@0.4.32:", when="@4:7")
