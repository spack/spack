# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyReretry(PythonPackage):
    """Easy to use retry decorator."""

    homepage = "https://github.com/leshchenko1979/reretry"
    pypi = "reretry/reretry-0.11.8.tar.gz"
    maintainers("charmoniumQ")

    license("Apache-2.0")

    version(
        "0.11.8",
        sha256="5ec1084cd9644271ee386d34cd5dd24bdb3e91d55961b076d1a31d585ad68a79",
        url="https://pypi.org/packages/66/11/e295e07d4ae500144177f875a8de11daa4d86b8246ab41c76a98ce9280ca/reretry-0.11.8-py2.py3-none-any.whl",
    )
    version(
        "0.11.1",
        sha256="54ecdd41b5ead5bc65a65cdeccf10cb3450f884168c08f4a9e0e089583890d10",
        url="https://pypi.org/packages/eb/75/592a6dabe116d0e54e95052aafaa703c1737c6a2d8c3a7f99cc6d1eeb5b8/reretry-0.11.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.11.7:")
