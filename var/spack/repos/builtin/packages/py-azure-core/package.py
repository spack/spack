# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureCore(PythonPackage):
    """Microsoft Azure Core Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/core/azure-core"
    pypi = "azure-core/azure-core-1.7.0.zip"

    version("1.26.1", sha256="223b0e90cbdd1f03c41b195b03239899843f20d00964dbb85e64386873414a2d")
    version("1.21.1", sha256="88d2db5cf9a135a7287dc45fdde6b96f9ca62c9567512a3bb3e20e322ce7deb2")
    version("1.7.0", sha256="a66da240a287f447f9867f54ba09ea235895cec13ea38c5f490ce4eedefdd75c")
    version("1.6.0", sha256="d10b74e783cff90d56360e61162afdd22276d62dc9467e657ae866449eae7648")

    # https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/core/azure-core/setup.py
    depends_on("py-setuptools", type="build")
    depends_on("py-requests@2.18.4:", type=("build", "run"))
    depends_on("py-six@1.6:", when="@:1.21", type=("build", "run"))
    depends_on("py-six@1.11:", when="@1.21:", type=("build", "run"))
    depends_on("py-typing-extensions@4.0.1:", when="@1.26:", type=("build", "run"))
