# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleAuth(PythonPackage):
    """This library simplifies using Google's various server-to-server
    authentication mechanisms to access Google APIs."""

    homepage = "https://github.com/GoogleCloudPlatform/google-auth-library-python"
    pypi = "google-auth/google-auth-1.6.3.tar.gz"

    license("Apache-2.0")

    version(
        "2.27.0",
        sha256="8e4bad367015430ff253fe49d500fdc3396c1a434db5740828c728e45bcce245",
        url="https://pypi.org/packages/82/41/7fb855444cead5b2213e053447ce3a0b7bf2c3529c443e0cf75b2f13b405/google_auth-2.27.0-py2.py3-none-any.whl",
    )
    version(
        "2.20.0",
        sha256="23b7b0950fcda519bfb6692bf0d5289d2ea49fc143717cc7188458ec620e63fa",
        url="https://pypi.org/packages/9a/1a/5866a7c6e16abc1df395e6d2b9808984d0905c747d75f5e20f1a052421d1/google_auth-2.20.0-py2.py3-none-any.whl",
    )
    version(
        "2.16.2",
        sha256="2fef3cf94876d1a0e204afece58bb4d83fb57228aaa366c64045039fda6770a2",
        url="https://pypi.org/packages/93/c4/16f8ad44ed7544244a9883f35cc99dc96378652a0ec7cc39028b1c697a1e/google_auth-2.16.2-py2.py3-none-any.whl",
    )
    version(
        "2.11.0",
        sha256="be62acaae38d0049c21ca90f27a23847245c9f161ff54ede13af2cb6afecbac9",
        url="https://pypi.org/packages/bb/6c/9b2dab3aff0dd9f685386598434dd8a0f205096b0a68d2c5e0c11be6f4b6/google_auth-2.11.0-py2.py3-none-any.whl",
    )
    version(
        "2.3.2",
        sha256="6e99f4b3b099feb50de20302f2f8987c1c36e80a3f856ce852675bdf7a0935d3",
        url="https://pypi.org/packages/89/a9/2264dce8fd1e4d55c73044d01c5a35565d179cd885174ad4fcdf0fa6ee36/google_auth-2.3.2-py2.py3-none-any.whl",
    )
    version(
        "1.6.3",
        sha256="20705f6803fd2c4d1cc2dcb0df09d4dfcb9a7d51fd59e94a3a28231fd93119ed",
        url="https://pypi.org/packages/c5/9b/ed0516cc1f7609fb0217e3057ff4f0f9f3e3ce79a369c6af4a6c5ca25664/google_auth-1.6.3-py2.py3-none-any.whl",
    )

    variant("aiohttp", default=False, when="@1.22.1:", description="Enables aiohttp support")

    with default_args(type="run"):
        depends_on("python@3.7:", when="@2.23:")
        depends_on("py-aiohttp@3.6.2:3", when="@1.22.1:+aiohttp")
        depends_on("py-cachetools@2:4", when="@1.10:2.3")
        depends_on("py-cachetools@2:", when="@:1.6,2.4:")
        depends_on("py-pyasn1-modules@0.2:", when="@1.3:")
        depends_on("py-requests@2.20:", when="@1.30.2:2.0.0.0,2.0.1:+aiohttp")
        depends_on("py-rsa@3.1.4:", when="@:1.6,1.17:")
        depends_on("py-setuptools@40.3:", when="@1.7:2.3")
        depends_on("py-six@1.9:", when="@:1,2.0.0.dev:2.0.0,2.3.1:2.22")
        depends_on("py-urllib3@:1", when="@2.18:2.23.0")
