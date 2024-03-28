# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTextwrap3(PythonPackage):
    """textwrap from Python 3.6 backport (plus a few tweaks)."""

    homepage = "https://github.com/jonathaneunice/textwrap3"
    pypi = "textwrap3/textwrap3-0.9.2.zip"

    version(
        "0.9.2",
        sha256="bf5f4c40faf2a9ff00a9e0791fed5da7415481054cef45bb4a3cfb1f69044ae0",
        url="https://pypi.org/packages/77/9c/a53e561d496ee5866bbeea4d3a850b3b545ed854f8a21007c1e0d872e94d/textwrap3-0.9.2-py2.py3-none-any.whl",
    )
