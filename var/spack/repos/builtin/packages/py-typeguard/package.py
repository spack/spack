# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypeguard(PythonPackage):
    """
    Run-time type checker for Python.
    """

    homepage = "https://github.com/agronholm/typeguard"
    pypi = "typeguard/typeguard-2.12.1.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version(
        "3.0.2",
        sha256="bbe993854385284ab42fd5bd3bee6f6556577ce8b50696d6cb956d704f286c8e",
        url="https://pypi.org/packages/e2/62/7d206b0ac6fcbb163215ecc622a54eb747f85ad86d14bc513a834442d0f6/typeguard-3.0.2-py3-none-any.whl",
    )
    version(
        "2.13.3",
        sha256="5e3e3be01e887e7eafae5af63d1f36c849aaa94e3a0112097312aabfa16284f1",
        url="https://pypi.org/packages/9a/bb/d43e5c75054e53efce310e79d63df0ac3f25e34c926be5dffb7d283fb2a8/typeguard-2.13.3-py3-none-any.whl",
    )
    version(
        "2.12.1",
        sha256="cc15ef2704c9909ef9c80e19c62fb8468c01f75aad12f651922acf4dbe822e02",
        url="https://pypi.org/packages/a0/88/2a1613174e7d05540358b2f19881f369bfe6ba737f0a673177e69eb623df/typeguard-2.12.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@3:4.1.2")
        depends_on("py-importlib-metadata@3.6:", when="@3: ^python@:3.9")
        depends_on("py-typing-extensions@4.4:", when="@3.0.0-rc1:4.0.0 ^python@:3.10")
