# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMachotools(PythonPackage):
    """Python package for editing Mach-O headers using macholib"""

    pypi = "machotools/machotools-0.2.0.tar.gz"

    version(
        "0.2.0",
        sha256="e4e93746bbc264554422da145164205e28a71feaefac41a01c8a3df8e64ed286",
        url="https://pypi.org/packages/f9/5c/de695e2b38a649a054570ea1aa7d70d0c2033b408bc32df20da7bf232c32/machotools-0.2.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-macholib", when="@0.2:")
