# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMsal(PythonPackage):
    """The Microsoft Authentication Library (MSAL) for Python library enables
    your app to access the Microsoft Cloud by supporting authentication of
    users with Microsoft Azure Active Directory accounts (AAD) and Microsoft
    Accounts (MSA) using industry standard OAuth2 and OpenID Connect."""

    homepage = "https://github.com/AzureAD/microsoft-authentication-library-for-python"
    pypi = "msal/msal-1.3.0.tar.gz"

    # If you get diamond dependency problems on py-pyjwt,
    # consider using v1.20.0, which has looser constraints
    version("1.20.0", sha256="78344cd4c91d6134a593b5e3e45541e666e37b747ff8a6316c3668dd1e6ab6b2")
    version("1.3.0", sha256="5442a3a9d006506e653d3c4daff40538bdf067bf07b6b73b32d1b231d5e77a92")
    version("1.0.0", sha256="ecbe3f5ac77facad16abf08eb9d8562af3bc7184be5d4d90c9ef4db5bde26340")

    # https://github.com/AzureAD/microsoft-authentication-library-for-python/blob/1.20.0/setup.py
    depends_on("py-setuptools", type="build")
    depends_on("py-requests@2.0.0:2", type=("build", "run"))
    depends_on("py-pyjwt@1.0.0:1+crypto", type=("build", "run"), when="@:1.3")
    depends_on("py-pyjwt@1.0.0:2+crypto", type=("build", "run"), when="@1.20:")
    depends_on("py-cryptography@0.6:40", type=("build", "run"), when="@1.20:")
