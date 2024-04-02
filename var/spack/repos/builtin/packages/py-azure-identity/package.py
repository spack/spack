# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureIdentity(PythonPackage):
    """Microsoft Azure Identity Library for Python."""

    homepage = (
        "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/identity/azure-identity"
    )
    pypi = "azure-identity/azure-identity-1.15.0.tar.gz"

    # 'azure.identity.aio' import doesn't work for some reason, leave out of
    # 'import_modules' list to ensure that tests still pass for other imports.
    import_modules = ["azure.identity", "azure.identity._internal", "azure.identity._credentials"]

    license("MIT")

    version(
        "1.15.0",
        sha256="a14b1f01c7036f11f148f22cd8c16e05035293d714458d6b44ddf534d93eb912",
        url="https://pypi.org/packages/30/10/5dbf755b368d10a28d55b06ac1f12512a13e88874a23db82defdea9a8cd9/azure_identity-1.15.0-py3-none-any.whl",
    )
    version(
        "1.14.1",
        sha256="3a5bef8e9c3281e864e869739be8d67424bff616cddae96b546ca2a5168d863d",
        url="https://pypi.org/packages/42/b6/e2757da4800e0f402b23d0ca6f1e88726263a501c198729cd865f45f3e22/azure_identity-1.14.1-py3-none-any.whl",
    )
    version(
        "1.13.0",
        sha256="bd700cebb80cd9862098587c29d8677e819beca33c62568ced6d5a8e5e332b82",
        url="https://pypi.org/packages/33/16/fa96a5e057d6842e95d94fc410896e061b3d3a2584d57e13fc58268df45f/azure_identity-1.13.0-py3-none-any.whl",
    )
    version(
        "1.12.0",
        sha256="2a58ce4a209a013e37eaccfd5937570ab99e9118b3e1acf875eed3a85d541b92",
        url="https://pypi.org/packages/ce/96/942f03d8a80e30e2289496c10d99e3a8b71f10c0b70b5337fd8ec2ae85e5/azure_identity-1.12.0-py3-none-any.whl",
    )
    version(
        "1.3.1",
        sha256="3775d5d244d65bde19d9ba76b95b1c82484a7a09f8b13140b106bc84df601d35",
        url="https://pypi.org/packages/dc/55/9b89cd436c145bc11cfb5ebabf2d4a7468a996104a2c26f2674eb3a7bb05/azure_identity-1.3.1-py2.py3-none-any.whl",
    )
    version(
        "1.2.0",
        sha256="4ce65058461c277991763ed3f121efc6b9eb9c2edefb62c414dfa85c814690d3",
        url="https://pypi.org/packages/c4/7a/9372cd51fc3408ede0fab950ef9a6518cad34ef36e199982bb1ddfa18512/azure_identity-1.2.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@1.11.0-beta3:1.15")
        depends_on("py-azure-core@1.23:", when="@1.15.0:")
        depends_on("py-azure-core@1.11:", when="@1.7.0-beta2:1.15.0-beta2")
        depends_on("py-azure-core@1.0.0:", when="@1.0.0:1.7.0-beta1")
        depends_on("py-cryptography@2.5:", when="@1.7.0-beta4:")
        depends_on("py-cryptography@2.1.4:", when="@:1.7.0-beta3")
        depends_on("py-msal@1.24.0:", when="@1.15.0-beta2:")
        depends_on("py-msal@1.20.0:", when="@1.13:1.15.0-beta1")
        depends_on("py-msal@1.12:", when="@1.7.0-beta2:1.12")
        depends_on("py-msal@1:", when="@1.0.1:1.4.0-beta3")
        depends_on("py-msal-extensions@0.3:", when="@1.10.0:")
        depends_on("py-msal-extensions@0.1.3:0.1", when="@1.0.1:1.4.0-beta3")
        depends_on("py-six@1.12:", when="@1.6:1.13")
        depends_on("py-six@1.6:", when="@1.0.0-beta2:1.5")

    # https://github.com/Azure/azure-sdk-for-python/blob/azure-identity_1.15.0/sdk/identity/azure-identity/setup.py
