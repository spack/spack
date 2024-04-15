# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJaracoFunctools(PythonPackage):
    """Functools like those found in stdlib"""

    homepage = "https://github.com/jaraco/jaraco.functools"
    pypi = "jaraco.functools/jaraco.functools-2.0.tar.gz"

    license("MIT")

    version(
        "2.0",
        sha256="e9e377644cee5f6f9128b4dab1631fca74981236e95a255f80e4292bcd2b5284",
        url="https://pypi.org/packages/12/a4/3e7366d0f5e75dcad7be88524c8cbd0f3a9fb1db243269550981740c57fe/jaraco.functools-2.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-more-itertools")
