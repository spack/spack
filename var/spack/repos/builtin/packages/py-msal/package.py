# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyMsal(PythonPackage):
    """The Microsoft Authentication Library (MSAL) for Python library enables
    your app to access the Microsoft Cloud by supporting authentication of
    users with Microsoft Azure Active Directory accounts (AAD) and Microsoft
    Accounts (MSA) using industry standard OAuth2 and OpenID Connect."""

    homepage = "https://github.com/AzureAD/microsoft-authentication-library-for-python"
    pypi = "msal/msal-1.3.0.tar.gz"

    version('1.9.0', sha256='c11a6f2a1f8ff522ebf415486b06bbd476582c7b26ee59f4a38a239f57e59249')
    version('1.8.0', sha256='1dcc737ca517df53438bc9a3fae97f17d93d7a93fa1389e6bc44e82eee81ab83')
    version('1.7.0', sha256='682a4d028e3a3406cd8ea50480655e4c62dcf541585fe94d7d679c8d3800f96b')
    version('1.6.0', sha256='c995de0710c31a918bd908cb750153b4d091fd6893e9ab73c685a53f950bbd96')
    version('1.5.1', sha256='7efb0256c96a7b2eadab49ce29ecdb91352a91440c12a40bed44303724b62fda')
    version('1.5.0', sha256='cc67d3a14850ba7e533ec5d05a4c23a34dd74a7fa5e0210daebef397b2009b0e')
    version('1.4.3', sha256='51b8e8e0d918d9b4813f006324e7c4e21eb76268dd4c1a06d811a3475ad4ac57')
    version('1.4.2', sha256='11beb3df29e75049ff1598784bf86e8fe4e84f4e079cfdf7a1775bfb7a564948')
    version('1.4.1', sha256='78e74e299bb9544f46505e20b6d98646b5b63ddd8a4f0ce4d06dbe720065c1a2')
    version('1.4.0', sha256='90672f4e4c2f57f7e61c47a57d3b45d95b76846ceb7e7a5faa58cdd3d781f48c')
    version('1.3.0', sha256='5442a3a9d006506e653d3c4daff40538bdf067bf07b6b73b32d1b231d5e77a92')
    version('1.0.0', sha256='ecbe3f5ac77facad16abf08eb9d8562af3bc7184be5d4d90c9ef4db5bde26340')

    depends_on('py-setuptools', type='build')
    depends_on('py-requests@2.0.0:2.999', type=('build', 'run'))
    depends_on('py-pyjwt@1.0.0:1.999+crypto', type=('build', 'run'))
