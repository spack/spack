# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyArchspec(PythonPackage):
    """A library for detecting, labeling and reasoning about
    microarchitectures.
    """

    homepage = "https://archspec.readthedocs.io/en/latest/"
    pypi = "archspec/archspec-0.2.0.tar.gz"

    maintainers("alalazo")

    license("Apache-2.0")

    version(
        "0.2.3",
        sha256="1b76fe2e75ee8750f0aac8c728af4beca1a95bdb5df246f4d39263664d6d301f",
        url="https://pypi.org/packages/36/a6/7f0f500ce427b19c25f8cc05ee8cff9fb635373d62ae39e446d6f789e882/archspec-0.2.3-py3-none-any.whl",
    )
    version(
        "0.2.2",
        sha256="1054b599abb66f4d141c7a278dd34beb5766b1c84c7595aab3907a5bf55ee258",
        url="https://pypi.org/packages/57/c1/45410841aaafe218632cfb9ae946eb4007ac8b5136bcae2987f0f56c7f56/archspec-0.2.2-py3-none-any.whl",
    )
    version(
        "0.2.1",
        sha256="e135481fc8384141ea2a18df9843045951717d8d029d60474a65d7d89b210821",
        url="https://pypi.org/packages/63/ae/333e7d216dda9134558ddc30792d96bfc58968ff5cc69b4ad9e02dfac654/archspec-0.2.1-py3-none-any.whl",
    )
    version(
        "0.2.0",
        sha256="6e820d5afc45fe051b7f2c07aa2ede68ea55ae67c27ba78ca795da8e3671f9cc",
        url="https://pypi.org/packages/9d/94/4c7f18613a052d5fbcb58bb1f938d3b1a04874c1464bfb63a26fe24435aa/archspec-0.2.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-click@8.0.0:", when="@0.2:0.2.0")
