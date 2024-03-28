# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAuxlib(PythonPackage):
    """Auxlib is an auxiliary library to the python standard library."""

    homepage = "https://github.com/kalefranz/auxlib"
    pypi = "auxlib/auxlib-0.0.43.tar.gz"

    license("ISC")

    version(
        "0.0.43",
        sha256="2864e48a0160beda799d404f2321faa0e3b9da33bf1384d5631a8329b1ad32d8",
        url="https://pypi.org/packages/31/a6/8bc9f3fac7563c9a728595f5aa8eeac1e42f6b66b003900d11db06f7b901/auxlib-0.0.43-py2.py3-none-any.whl",
    )
