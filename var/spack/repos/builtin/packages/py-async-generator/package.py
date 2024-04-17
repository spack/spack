# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsyncGenerator(PythonPackage):
    """Provides async generator functionality to python 3.5."""

    pypi = "async_generator/async_generator-1.10.tar.gz"

    license("Apache-2.0")

    version(
        "1.10",
        sha256="01c7bf666359b4967d2cda0000cc2e4af16a0ae098cbffcb8472fb9e8ad6585b",
        url="https://pypi.org/packages/71/52/39d20e03abd0ac9159c162ec24b93fbcaa111e8400308f2465432495ca2b/async_generator-1.10-py3-none-any.whl",
    )
