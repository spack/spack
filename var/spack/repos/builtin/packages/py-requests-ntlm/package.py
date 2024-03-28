# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRequestsNtlm(PythonPackage):
    """This package allows for HTTP NTLM authentication using the requests library."""

    homepage = "https://github.com/requests/requests-ntlm"
    pypi = "requests_ntlm/requests_ntlm-1.1.0.tar.gz"

    license("ISC")

    version(
        "1.1.0",
        sha256="1eb43d1026b64d431a8e0f1e8a8c8119ac698e72e9b95102018214411a8463ea",
        url="https://pypi.org/packages/03/4b/8b9a1afde8072c4d5710d9fa91433d504325821b038e00237dc8d6d833dc/requests_ntlm-1.1.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-cryptography@1.3:", when="@1.1:")
        depends_on("py-ntlm-auth@1.0.2:", when="@1:1.1")
        depends_on("py-requests@2:", when="@0.3:")
