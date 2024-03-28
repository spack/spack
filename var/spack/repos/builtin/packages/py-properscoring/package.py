# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyProperscoring(PythonPackage):
    """Proper scoring rules in Python."""

    homepage = "https://github.com/properscoring/properscoring"
    pypi = "properscoring/properscoring-0.1.tar.gz"

    license("Apache-2.0")

    version(
        "0.1",
        sha256="f84d5b06c13549d0171ce52ad7b45c6f5726ac44b733d24af5c60654cbb821dc",
        url="https://pypi.org/packages/0a/ff/51706ba1a029d0f2df0322543793d3bf1383de9dc567d23886144cb21bef/properscoring-0.1-py2.py3-none-any.whl",
    )
