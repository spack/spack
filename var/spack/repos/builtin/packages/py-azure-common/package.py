# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureCommon(PythonPackage):
    """Microsoft Azure Client Library for Python (Common)."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-common/azure-common-1.1.25.zip"

    version(
        "1.1.25",
        sha256="fd02e4256dc9cdd2d4422bc795bdca2ef302f7a86148b154fbf4ea1f09da400a",
        url="https://pypi.org/packages/e5/4d/d000fc3c5af601d00d55750b71da5c231fcb128f42ac95b208ed1091c2c1/azure_common-1.1.25-py2.py3-none-any.whl",
    )
