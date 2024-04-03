# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGlobusSdk(PythonPackage):
    """
    Globus SDK for Python
    """

    homepage = "https://github.com/globus/globus-sdk-python"
    pypi = "globus-sdk/globus-sdk-3.0.2.tar.gz"

    maintainers("hategan")

    license("Apache-2.0")

    version(
        "3.10.1",
        sha256="e8073dd8db5bcd9c14d0f9dc5c543d4bfe25bfe96d6aab34a9c4961d985ed59f",
        url="https://pypi.org/packages/86/74/9dce30b2e12d8f26c4270667b09c5cd1ab0f3bada696ae65717893258a51/globus_sdk-3.10.1-py3-none-any.whl",
    )
    version(
        "3.10.0",
        sha256="f73d15cf88463aac9a9f77b8c4f601e11adfcbd4ecc77910a144dd251ed90551",
        url="https://pypi.org/packages/61/e2/a491b39a861df113d99f0ddd6e6f68aab416d6df7c9d52ed8cd98ab5389e/globus_sdk-3.10.0-py3-none-any.whl",
    )
    version(
        "3.9.0",
        sha256="a196070b549d6af534a7fa8a180eae6ab84c0745959d5ee2d3863705eef9c7fc",
        url="https://pypi.org/packages/a1/19/83dd4110d789eabeec942bfd39d992f037fb2875f50faf8c142dafa99b9a/globus_sdk-3.9.0-py3-none-any.whl",
    )
    version(
        "3.8.0",
        sha256="8ede91296c793eb2a1a9ec56c3660d257b31afb28bf49e402f3589df28f17afb",
        url="https://pypi.org/packages/af/18/8cbd7b20e660c29b79b86afaf282592ee382e3df5acaa25e588aa74bf2f5/globus_sdk-3.8.0-py3-none-any.whl",
    )
    version(
        "3.7.0",
        sha256="ba2d85b61374394a096814cbddee510b89883b68803e47e6cf4247324ea57fa6",
        url="https://pypi.org/packages/29/40/9041132e1b12577a79a13811f5f1da5de5c3728bf0f23c6c2ade21150894/globus_sdk-3.7.0-py3-none-any.whl",
    )
    version(
        "3.0.2",
        sha256="03b1a24fc0f9080163999bb651c8ce2a35a6c9fcdf7f57fe913978d2eed31557",
        url="https://pypi.org/packages/b2/bd/078c44638ae236c56c8a942de7743d0c44074933fe7426dff88f803777b0/globus_sdk-3.0.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-cryptography@3.3.1:3.3,3.4.1:", when="@3.1:")
        depends_on("py-cryptography@2:3.3,3.4.1:3", when="@3.0.2:3.0")
        depends_on("py-pyjwt@2.0.0:+crypto")
        depends_on("py-requests@2.19.1:", when="@3.0.2:")
        depends_on("py-typing-extensions@4:", when="@3.4.1: ^python@:3.9")
