# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNamex(PythonPackage):
    """A simple utility to separate the implementation of your Python package
    and its public API surface."""

    pypi = "namex/namex-0.0.7.tar.gz"

    license("Apache-2.0")

    version(
        "0.0.7",
        sha256="8a4f062945f405d77cb66b907f16aa2fd83681945e998be840eb6c4154d40108",
        url="https://pypi.org/packages/cd/43/b971880e2eb45c0bee2093710ae8044764a89afe9620df34a231c6f0ecd2/namex-0.0.7-py3-none-any.whl",
    )
