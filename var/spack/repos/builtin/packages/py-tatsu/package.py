# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTatsu(PythonPackage):
    """TatSu (the successor to Grako) is a tool that takes grammars in
    a variation of EBNF as input, and outputs memoizing (Packrat) PEG
    parsers in Python."""

    homepage = "https://github.com/neogeny/tatsu"
    pypi = "TatSu/TatSu-4.4.0.zip"

    license("BSD-2-Clause")

    version(
        "4.4.0",
        sha256="c9211eeee9a2d4c90f69879ec0b518b1aa0d9450249cb0dd181f5f5b18be0a92",
        url="https://pypi.org/packages/1b/36/00664e684e4bba5730db661847447bbcfe789008a154755013e5f457b648/TatSu-4.4.0-py2.py3-none-any.whl",
    )

    variant("future_regex", default=True, description="Use regex implementation")

    # optional dependency, otherwise falls back to standard implementation
