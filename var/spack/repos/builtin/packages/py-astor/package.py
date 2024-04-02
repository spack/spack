# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyAstor(PythonPackage):
    """
    astor is designed to allow easy manipulation of Python source via the AST.
    """

    pypi = "astor/astor-0.8.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.8.1",
        sha256="070a54e890cefb5b3739d19f30f5a5ec840ffc9c50ffa7d23cc9fc1a38ebbfc5",
        url="https://pypi.org/packages/c3/88/97eef84f48fa04fbd6750e62dcceafba6c63c81b7ac1420856c8dcc0a3f9/astor-0.8.1-py2.py3-none-any.whl",
    )
    version(
        "0.8.0",
        sha256="0e41295809baf43ae8303350e031aff81ae52189b6f881f36d623fa8b2f1960e",
        url="https://pypi.org/packages/d1/4f/950dfae467b384fc96bc6469de25d832534f6b4441033c39f914efd13418/astor-0.8.0-py2.py3-none-any.whl",
    )
    version(
        "0.6",
        sha256="5b5d375c4e3d2d0f52fcfe0128bc064d928f36fe622b52e4127a631803fbe2ab",
        url="https://pypi.org/packages/69/32/e8a3285c0be9ce7ef42bfa302b995109036994713344b6baeed88bb12146/astor-0.6-py2.py3-none-any.whl",
    )

    # Build fails with newer versions of setuptools
    # https://github.com/berkerpeksag/astor/issues/162
    # https://github.com/berkerpeksag/astor/pull/163
