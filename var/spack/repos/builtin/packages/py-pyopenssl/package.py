# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyopenssl(PythonPackage):
    """High-level wrapper around a subset of the OpenSSL library.

    Note: The Python Cryptographic Authority strongly suggests the use of
    pyca/cryptography where possible. If you are using pyOpenSSL for anything
    other than making a TLS connection you should move to cryptography and
    drop your pyOpenSSL dependency."""

    homepage = "https://pyopenssl.org/"
    pypi = "pyOpenSSL/pyOpenSSL-19.0.0.tar.gz"

    license("Apache-2.0")

    version(
        "23.2.0",
        sha256="24f0dc5227396b3e831f4c7f602b950a5e9833d292c8e4a2e06b709292806ae2",
        url="https://pypi.org/packages/f0/e2/f8b4f1c67933a4907e52228241f4bd52169f3196b70af04403b29c63238a/pyOpenSSL-23.2.0-py3-none-any.whl",
    )
    version(
        "22.1.0",
        sha256="b28437c9773bb6c6958628cf9c3bebe585de661dba6f63df17111966363dd15e",
        url="https://pypi.org/packages/00/3f/ea5cfb789dddb327e6d2cf9377c36d9d8607af85530af0e7001165587ae7/pyOpenSSL-22.1.0-py3-none-any.whl",
    )
    version(
        "20.0.1",
        sha256="818ae18e06922c066f777a33f1fca45786d85edfe71cd043de6379337a7f274b",
        url="https://pypi.org/packages/b2/5e/06351ede29fd4899782ad335c2e02f1f862a887c20a3541f17c3fa1a3525/pyOpenSSL-20.0.1-py2.py3-none-any.whl",
    )
    version(
        "19.0.0",
        sha256="c727930ad54b10fc157015014b666f2d8b41f70c0d03e83ab67624fd3dd5d1e6",
        url="https://pypi.org/packages/01/c8/ceb170d81bd3941cbeb9940fc6cc2ef2ca4288d0ca8929ea4db5905d904d/pyOpenSSL-19.0.0-py2.py3-none-any.whl",
    )
    version(
        "18.0.0",
        sha256="26ff56a6b5ecaf3a2a59f132681e2a80afcc76b4f902f612f518f92c2a1bf854",
        url="https://pypi.org/packages/96/af/9d29e6bd40823061aea2e0574ccb2fcf72bfd6130ce53d32773ec375458c/pyOpenSSL-18.0.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-cryptography@38:39,40.0.2:41", when="@23.2")
        depends_on("py-cryptography@38", when="@22.1:22")
        depends_on("py-cryptography@3.2:", when="@20")
        depends_on("py-cryptography@2.3:", when="@19:19.0")
        depends_on("py-cryptography@2.2.1:", when="@18")
        depends_on("py-six@1.5.2:", when="@:21")

    conflicts("^py-cryptography@40:40.0.1", when="@23.2:")

    # Historical dependencies
