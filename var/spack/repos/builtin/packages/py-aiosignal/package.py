# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAiosignal(PythonPackage):
    """A project to manage callbacks in asyncio projects."""

    homepage = "https://aiosignal.readthedocs.io/"
    pypi = "aiosignal/aiosignal-1.2.0.tar.gz"

    license("Apache-2.0")

    version(
        "1.2.0",
        sha256="26e62109036cd181df6e6ad646f91f0dcfd05fe16d0cb924138ff2ab75d64e3a",
        url="https://pypi.org/packages/3b/87/fe94898f2d44a93a35d5aa74671ed28094d80753a1113d68b799fab6dc22/aiosignal-1.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-frozenlist@1.1:", when="@1.1:")
