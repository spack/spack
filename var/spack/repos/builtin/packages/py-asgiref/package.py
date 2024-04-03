# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsgiref(PythonPackage):
    """ASGI specification and utilities."""

    homepage = "https://asgi.readthedocs.io/en/latest/"
    url = "https://github.com/django/asgiref/archive/3.2.7.tar.gz"

    license("BSD-3-Clause")

    version(
        "3.5.2",
        sha256="1d2880b792ae8757289136f1db2b7b99100ce959b2aa57fd69dab783d05afac4",
        url="https://pypi.org/packages/af/6d/ea3a5c3027c3f14b0321cd4f7e594c776ebe64e4b927432ca6917512a4f7/asgiref-3.5.2-py3-none-any.whl",
    )
    version(
        "3.5.0",
        sha256="88d59c13d634dcffe0510be048210188edd79aeccb6a6c9028cdad6f31d730a9",
        url="https://pypi.org/packages/0b/9f/5f3b91391578312827561b669a0397d58535b4e82966c8f1667525c7d563/asgiref-3.5.0-py3-none-any.whl",
    )
    version(
        "3.2.7",
        sha256="9ca8b952a0a9afa61d30aa6d3d9b570bb3fd6bafcf7ec9e6bed43b936133db1c",
        url="https://pypi.org/packages/68/00/25013f7310a56d17e1ab6fd885d5c1f216b7123b550d295c93f8e29d372a/asgiref-3.2.7-py2.py3-none-any.whl",
    )
    version(
        "3.2.6",
        sha256="9c65b42045910c159ad41fc33692a8a6e6e154d8d05244ea69a0cbc617edad31",
        url="https://pypi.org/packages/e2/ea/37fac52810bfa225c867cd05766d80c12799f0a0d38a552dfe0ba7d02a90/asgiref-3.2.6-py2.py3-none-any.whl",
    )
    version(
        "3.2.5",
        sha256="3e4192eaec0758b99722f0b0666d5fbfaa713054d92e8de5b58ba84ec5ce696f",
        url="https://pypi.org/packages/bc/a9/90e110710d44289d807b5604bcd18419ece1a6f88e9a2489d3de4718a20b/asgiref-3.2.5-py2.py3-none-any.whl",
    )
    version(
        "3.2.4",
        sha256="5e60ea919b37e5b9d8896d802c0dbbe41b16ea6719e5695a43496ef43e5b19ac",
        url="https://pypi.org/packages/80/c6/03bd9a8568952c275e8b2ee4ab3ac744d5fff7a8d2b5bba5b93715ba742e/asgiref-3.2.4-py2.py3-none-any.whl",
    )
    version(
        "3.2.3",
        sha256="ea448f92fc35a0ef4b1508f53a04c4670255a3f33d22a81c8fc9c872036adbe5",
        url="https://pypi.org/packages/a5/cb/5a235b605a9753ebcb2730c75e610fb51c8cab3f01230080a8229fa36adb/asgiref-3.2.3-py2.py3-none-any.whl",
    )
    version(
        "3.2.2",
        sha256="a4ce726e6ef49cca13642ff49588530ebabcc47c669c7a95af37ea5a74b9b823",
        url="https://pypi.org/packages/d0/39/42344b1060cfb5542eecef3ce6dda3d2d5a89a660716ed5980635985f2a7/asgiref-3.2.2-py2.py3-none-any.whl",
    )
    version(
        "3.2.1",
        sha256="ceac3968866501249712f482ae807605246cfae8293a70de29417868ddef673c",
        url="https://pypi.org/packages/4c/b9/9eb9762c9b43754d49e6b85625c1a5a45673a3083c742be00d8721839b01/asgiref-3.2.1-py2.py3-none-any.whl",
    )
    version(
        "3.2.0",
        sha256="abfe78df4bdefdbdc6902b1900c14e60b4cd7fea2ce218b5f12d998a46a9eb18",
        url="https://pypi.org/packages/fb/58/27f90221f17bbda171d345f06009749004b60aea53a723443903bd99673d/asgiref-3.2.0-py2.py3-none-any.whl",
    )
    version(
        "3.1.4",
        sha256="b718a9d35e204a96e2456c2271b0ef12e36124c363b3a8fd1d626744f23192aa",
        url="https://pypi.org/packages/ce/2e/dd4b5afc37d595fc44def4f365cc8ee080a4962a0eb1e05e79da65a8e074/asgiref-3.1.4-py2.py3-none-any.whl",
    )
    version(
        "3.1.3",
        sha256="34227987327d13bc4b19d338faa6fed8a25cea79cca2e9e50490d212f56470f8",
        url="https://pypi.org/packages/c2/c4/db607d2dcdd1d88763528de1066dec9f36cca470c1d101de5cc35c90b0b9/asgiref-3.1.3-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@3.5:3.7")
        depends_on("py-typing-extensions", when="@3.3.2:3.6 ^python@:3.7")
