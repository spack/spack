# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyA2wsgi(PythonPackage):
    """Convert WSGI app to ASGI app or ASGI app to WSGI app."""

    homepage = "https://github.com/abersheeran/a2wsgi"
    pypi = "a2wsgi/a2wsgi-1.6.0.tar.gz"

    license("Apache-2.0")

    version(
        "1.7.0",
        sha256="d26be288b2a5f368181b6e0d1cfc3c2a4180732cca10e9cc4b9bc333235b8d80",
        url="https://pypi.org/packages/c5/b8/ccf880c8a3e564283f0ed1b4268e13e4cb9075491b0863f9a2bf83d5e58a/a2wsgi-1.7.0-py3-none-any.whl",
    )
    version(
        "1.6.0",
        sha256="ee8507d07fd86b781d3e039fe458366e2127bd2251b47fcbedadbf013095a21e",
        url="https://pypi.org/packages/b2/fb/4bb5451ee0a98194267a99acb060f9113c9b13796020c1a63eadd637acdb/a2wsgi-1.6.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@1.7")
