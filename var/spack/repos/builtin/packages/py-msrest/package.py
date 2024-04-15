# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMsrest(PythonPackage):
    """AutoRest swagger generator Python client runtime."""

    homepage = "https://github.com/Azure/msrest-for-python"
    pypi = "msrest/msrest-0.7.1.zip"

    version(
        "0.7.1",
        sha256="21120a810e1233e5e6cc7fe40b474eeb4ec6f757a15d7cf86702c369f9567c32",
        url="https://pypi.org/packages/15/cf/f2966a2638144491f8696c27320d5219f48a072715075d168b31d3237720/msrest-0.7.1-py3-none-any.whl",
    )
    version(
        "0.6.21",
        sha256="c840511c845330e96886011a236440fafc2c9aff7b2df9c0a92041ee2dee3782",
        url="https://pypi.org/packages/e8/cc/6c96bfb3d3cf4c3bdedfa6b46503223f4c2a4fa388377697e0f8082a4fed/msrest-0.6.21-py2.py3-none-any.whl",
    )
    version(
        "0.6.16",
        sha256="88b31e937eba95bda5b9a910b28498fdc130718bb5f8dd98a6af0d333670c897",
        url="https://pypi.org/packages/34/68/fa7892bd8bb46eba90f7a2ffbc6725ee0b2e302444677377d0853a1c840f/msrest-0.6.16-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-azure-core@1.24:", when="@0.7:")
        depends_on("py-certifi@2017.4:")
        depends_on("py-isodate@0.6:")
        depends_on("py-requests@2.16:")
        depends_on("py-requests-oauthlib@0.5:")
