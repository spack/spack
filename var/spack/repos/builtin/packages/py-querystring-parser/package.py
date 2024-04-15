# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQuerystringParser(PythonPackage):
    """QueryString parser that correctly handles nested dictionaries."""

    homepage = "https://pypi.org/project/querystring-parser/"
    pypi = "querystring-parser/querystring_parser-1.2.4.tar.gz"

    version(
        "1.2.4",
        sha256="d2fa90765eaf0de96c8b087872991a10238e89ba015ae59fedfed6bd61c242a0",
        url="https://pypi.org/packages/88/6b/572b2590fd55114118bf08bde63c0a421dcc82d593700f3e2ad89908a8a9/querystring_parser-1.2.4-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-six", when="@1.2.4:")
