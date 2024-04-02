# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTestpath(PythonPackage):
    """Testpath is a collection of utilities for Python code working with
    files and commands."""

    homepage = "https://github.com/jupyter/testpath"
    pypi = "testpath/testpath-0.4.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.6.0",
        sha256="8ada9f80a2ac6fb0391aa7cdb1a7d11cfa8429f693eda83f74dde570fe6fa639",
        url="https://pypi.org/packages/86/43/1ebfb29c2ca1df2bdb33dbcb2b526b77ee96873ba7b9e25650ddd4ae7156/testpath-0.6.0-py3-none-any.whl",
    )
    version(
        "0.5.0",
        sha256="8044f9a0bab6567fc644a3593164e872543bb44225b0e24846e2c89237937589",
        url="https://pypi.org/packages/ac/87/5422f6d056bfbded920ccf380a65de3713a3b95a95ba2255be2a3fb4f464/testpath-0.5.0-py3-none-any.whl",
    )
    version(
        "0.4.2",
        sha256="46c89ebb683f473ffe2aab0ed9f12581d4d078308a3cb3765d79c6b2317b0109",
        url="https://pypi.org/packages/be/a4/162f9ebb6489421fe46dcca2ae420369edfee4b563c668d93cb4605d12ba/testpath-0.4.2-py2.py3-none-any.whl",
    )
