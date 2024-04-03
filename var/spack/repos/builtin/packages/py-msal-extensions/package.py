# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMsalExtensions(PythonPackage):
    """The Microsoft Authentication Extensions for Python offers secure
    mechanisms for client applications to perform cross-platform token cache
    serialization and persistence. It gives additional support to the
    Microsoft Authentication Library for Python (MSAL)."""

    homepage = "https://github.com/AzureAD/microsoft-authentication-library-for-python"
    pypi = "msal-extensions/msal-extensions-0.2.2.tar.gz"

    license("MIT")

    version(
        "1.0.0",
        sha256="91e3db9620b822d0ed2b4d1850056a0f133cba04455e62f11612e40f5502f2ee",
        url="https://pypi.org/packages/52/34/a8995d6f0fa626ff6b28dbd9c90f6c2a46bd484bc7ab343d078b0c6ff1a7/msal_extensions-1.0.0-py2.py3-none-any.whl",
    )
    version(
        "0.2.2",
        sha256="f092246787145ec96d6c3c9f7bedfb837830fe8a79b56180e531fbf28b8de532",
        url="https://pypi.org/packages/33/da/eed514cb6902405c5c11a03f1e65adbd95e2c26d9b22eae390eddb561201/msal_extensions-0.2.2-py2.py3-none-any.whl",
    )
    version(
        "0.1.3",
        sha256="c5a32b8e1dce1c67733dcdf8aa8bebcff5ab123e779ef7bc14e416bd0da90037",
        url="https://pypi.org/packages/21/9b/8bc67822e98573fe0460e30ad0202ab9e0638a42878041c65a6fe857babe/msal_extensions-0.1.3-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-msal@0.4.1:", when="@0.1.3:")
        depends_on("py-portalocker@1.6:", when="@0.3.1: platform=windows")
        depends_on("py-portalocker@1:", when="@0.3.1: platform=linux")
        depends_on("py-portalocker@1:", when="@0.3.1: platform=freebsd")
        depends_on("py-portalocker@1:", when="@0.3.1: platform=darwin")
        depends_on("py-portalocker@1:", when="@0.3.1: platform=cray")
        depends_on("py-portalocker@1.6:1", when="@0.2.1:0.3.0 platform=windows")
        depends_on("py-portalocker@1", when="@0.2.1:0.3.0 platform=linux")
        depends_on("py-portalocker@1", when="@0.2.1:0.3.0 platform=freebsd")
        depends_on("py-portalocker@1", when="@0.2.1:0.3.0 platform=darwin")
        depends_on("py-portalocker@1", when="@0.2.1:0.3.0 platform=cray")
        depends_on("py-portalocker@1", when="@:0.1")

    # https://github.com/AzureAD/microsoft-authentication-extensions-for-python/blob/1.0.0/setup.py
    # This is the earliest version to work for Windows and non-Windows
