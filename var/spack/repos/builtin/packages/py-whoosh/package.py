# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWhoosh(PythonPackage):
    """Fast, pure-Python full text indexing, search, and spell checking library."""

    homepage = "https://whoosh.readthedocs.io"
    pypi = "Whoosh/Whoosh-2.7.4.tar.gz"

    license("BSD-2-Clause-FreeBSD")

    version(
        "2.7.4",
        sha256="aa39c3c3426e3fd107dcb4bde64ca1e276a65a889d9085a6e4b54ba82420a852",
        url="https://pypi.org/packages/ba/19/24d0f1f454a2c1eb689ca28d2f178db81e5024f42d82729a4ff6771155cf/Whoosh-2.7.4-py2.py3-none-any.whl",
    )
