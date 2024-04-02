# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsynctest(PythonPackage):
    """The package asynctest is built on top of the standard unittest module
    and cuts down boilerplate code when testing libraries for asyncio."""

    homepage = "https://asynctest.readthedocs.io"
    pypi = "asynctest/asynctest-0.13.0.tar.gz"

    license("Apache-2.0")

    version(
        "0.13.0",
        sha256="5da6118a7e6d6b54d83a8f7197769d046922a44d2a99c21382f0a6e4fadae676",
        url="https://pypi.org/packages/e8/b6/8d17e169d577ca7678b11cd0d3ceebb0a6089a7f4a2de4b945fe4b1c86db/asynctest-0.13.0-py3-none-any.whl",
    )
