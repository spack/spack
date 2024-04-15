# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMypyExtensions(PythonPackage):
    """Experimental type system extensions for programs checked with the
    mypy typechecker."""

    homepage = "https://github.com/python/mypy_extensions"
    pypi = "mypy-extensions/mypy_extensions-0.4.3.tar.gz"

    license("MIT")

    version(
        "1.0.0",
        sha256="4392f6c0eb8a5668a69e23d168ffa70f0be9ccfd32b5cc2d26a34ae5b844552d",
        url="https://pypi.org/packages/2a/e2/5d3f6ada4297caebe1a2add3b126fe800c96f56dbe5d1988a2cbe0b267aa/mypy_extensions-1.0.0-py3-none-any.whl",
    )
    version(
        "0.4.3",
        sha256="090fedd75945a69ae91ce1303b5824f428daf5a028d2f6ab8a299250a846f15d",
        url="https://pypi.org/packages/5c/eb/975c7c080f3223a5cdaff09612f3a5221e4ba534f7039db34c35d95fa6a5/mypy_extensions-0.4.3-py2.py3-none-any.whl",
    )
