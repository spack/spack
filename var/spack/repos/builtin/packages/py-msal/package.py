# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
    pypi = "msal/msal-1.26.0.tar.gz"

    license("MIT")

    version(
        "1.26.0",
        sha256="be77ba6a8f49c9ff598bbcdc5dfcf1c9842f3044300109af738e8c3e371065b5",
        url="https://pypi.org/packages/b7/61/2756b963e84db6946e4b93a8e288595106286fc11c7129fcb869267ead67/msal-1.26.0-py2.py3-none-any.whl",
    )
    version(
        "1.20.0",
        sha256="d2f1c26368ecdc28c8657d457352faa0b81b1845a7b889d8676787721ba86792",
        url="https://pypi.org/packages/53/51/b0874200ae0b926d83e402a5689b81310f49743b78e6457dbab85d0b354f/msal-1.20.0-py2.py3-none-any.whl",
    )
    version(
        "1.3.0",
        sha256="a620afb65c468b78ce26d7a724c7ebc5d350ffcb57e1d18dc722e5ca1244673b",
        url="https://pypi.org/packages/8a/0c/b88d529caf2fa8658cae9b616d27b4ecba203c15981c29c89ef9e57b71b4/msal-1.3.0-py2.py3-none-any.whl",
    )
    version(
        "1.0.0",
        sha256="c944b833bf686dfbc973e9affdef94b77e616cb52ab397e76cde82e26b8a3373",
        url="https://pypi.org/packages/a9/7c/bc473b3fe76d466362e5b84b4b165b18a427604a9582a9bca61c1545d872/msal-1.0.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-cryptography@0.6:", when="@1.23:1.27.0-beta2")
        depends_on("py-cryptography@0.6:40", when="@1.19,1.20.0:1.21")
        depends_on("py-pyjwt@1:+crypto", when="@1.9:")
        depends_on("py-pyjwt@1+crypto", when="@:1.8")
        depends_on("py-requests@2:")

    # https://github.com/AzureAD/microsoft-authentication-library-for-python/blob/1.26.0/setup.cfg
