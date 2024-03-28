# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPuremagic(PythonPackage):
    """puremagic is a pure python module that will identify a file based off its magic numbers."""

    homepage = "https://github.com/cdgriffith/puremagic"
    pypi = "puremagic/puremagic-1.10.tar.gz"

    license("MIT")

    version(
        "1.14",
        sha256="40e32752827f2d0cea7e6f11454fab2b4bd440582af83d8a47bf403ab42364fa",
        url="https://pypi.org/packages/14/20/c05ea76f4448c483f1c4486504bd6d98adeefb7ef597190f76d599ef8a5e/puremagic-1.14-py3-none-any.whl",
    )
    version(
        "1.10",
        sha256="3603ac88bfa06689b4a3a2e90ef30f8cc5769df2f269bf546620bfe6b18c06d6",
        url="https://pypi.org/packages/d5/6e/62d1cef9a0d8edf2d9c44b0a1b91b0b29b66fb693c94af278a0c76ddfd8c/puremagic-1.10-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-argparse", when="@1.4:1.10")
