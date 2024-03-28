# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGunicorn(PythonPackage):
    """WSGI HTTP Server for UNIX"""

    homepage = "https://gunicorn.org"
    pypi = "gunicorn/gunicorn-20.1.0.tar.gz"

    license("MIT")

    version(
        "20.1.0",
        sha256="9dcc4547dbb1cb284accfb15ab5667a0e5d1881cc443e0677b4882a4067a807e",
        url="https://pypi.org/packages/e4/dd/5b190393e6066286773a67dfcc2f9492058e9b57c4867a95f1ba5caf0a83/gunicorn-20.1.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-setuptools@3:", when="@20")
