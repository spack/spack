# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMarshmallow(PythonPackage):
    """marshmallow is an ORM/ODM/framework-agnostic library for converting
    complex datatypes, such as objects, to and from native Python datatypes."""

    homepage = "https://github.com/marshmallow-code/marshmallow"
    pypi = "marshmallow/marshmallow-3.15.0.tar.gz"

    maintainers("haralmha")

    license("MIT")

    version(
        "3.19.0",
        sha256="93f0958568da045b0021ec6aeb7ac37c81bfcccbb9a0e7ed8559885070b3a19b",
        url="https://pypi.org/packages/ae/53/980a20d789029329fdf1546c315f9c92bf862c7f3e7294e3667afcc464f5/marshmallow-3.19.0-py3-none-any.whl",
    )
    version(
        "3.15.0",
        sha256="ff79885ed43b579782f48c251d262e062bce49c65c52412458769a4fb57ac30f",
        url="https://pypi.org/packages/d3/87/a83cac9b3b10b1324196611162c3c434f1fe722a9ae50c642c20d5476022/marshmallow-3.15.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@3.15:3.19")
        depends_on("py-packaging@17:", when="@3.16:")
        depends_on("py-packaging", when="@3.15")
