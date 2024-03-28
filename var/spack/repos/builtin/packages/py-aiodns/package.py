# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAiodns(PythonPackage):
    """Simple DNS resolver for asyncio.It provides a simple way for
    doing asynchronous DNS resolutions using pycares."""

    homepage = "https://pypi.org/project/aiodns/"
    pypi = "aiodns/aiodns-2.0.0.tar.gz"

    license("MIT")

    version(
        "2.0.0",
        sha256="aaa5ac584f40fe778013df0aa6544bf157799bd3f608364b451840ed2c8688de",
        url="https://pypi.org/packages/da/01/8f2d49b441573fd2478833bdba91cf0b853b4c750a1fbb9e98de1b94bb22/aiodns-2.0.0-py2.py3-none-any.whl",
    )
    version(
        "1.2.0",
        sha256="970688599fcb7d65334ec490a94a51afd634ae2de8a2138d21e2ffbbddc12718",
        url="https://pypi.org/packages/c0/9d/82d910965520ac17956a4b412e36298466de1b87a8fd0ab6dea601cdb8aa/aiodns-1.2.0-py2.py3-none-any.whl",
    )
    version(
        "1.1.1",
        sha256="99d0652f2c02f73bfa646bf44af82705260a523014576647d7959e664830b26b",
        url="https://pypi.org/packages/bd/f5/b69cb930fd5ab0569396659afe3f3c0d37d4098e5d0ba6afdf6fd9388cb0/aiodns-1.1.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pycares@3.0.0:", when="@2.0.0:2")
        depends_on("py-pycares@1:", when="@1.1:1")
        depends_on("py-typing", when="@1.2:2.0.0-beta0")
