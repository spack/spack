# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPybtexDocutils(PythonPackage):
    """A docutils backend for pybtex."""

    pypi = "pybtex-docutils/pybtex-docutils-0.2.1.tar.gz"

    license("MIT")

    version(
        "1.0.0",
        sha256="8a2ca2d89b70be3a722d73aeb64d57065c79000f54719672dd9a9a86288d13f7",
        url="https://pypi.org/packages/6a/4b/060b0c0e3b18ae927fa6400233661b3af064571dba4fac92372030ed640b/pybtex_docutils-1.0.0-py3-none-any.whl",
    )
    version(
        "0.2.2",
        sha256="4beb8c36f4f4a5a3f437cc2ff7dea8c1c7fe655d79c1229cb432af141884875b",
        url="https://pypi.org/packages/e9/97/066aa09efc1a1f969ffc6ca0e697787a3b8eb9e847a9b5973c0f73119318/pybtex_docutils-0.2.2-py2.py3-none-any.whl",
    )
    version(
        "0.2.1",
        sha256="920ae9850750dd61abe00d9fd88f4a5f9099e40af0b84b2119b8b44a479115d2",
        url="https://pypi.org/packages/5f/7f/f2107bd9b1cc38a83cd18e9ab8608d8905e35fbd6e936e32354531e3ae75/pybtex_docutils-0.2.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-docutils@0.8:", when="@0.2.1:1.0.2")
        depends_on("py-pybtex@0.16:", when="@0.2.1:")
        depends_on("py-six", when="@0.2.1:0")
