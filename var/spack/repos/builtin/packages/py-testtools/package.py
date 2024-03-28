# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTesttools(PythonPackage):
    """Extensions to the Python standard library unit testing framework."""

    homepage = "https://github.com/testing-cabal/testtools"
    pypi = "testtools/testtools-2.3.0.tar.gz"

    license("MIT")

    version(
        "2.3.0",
        sha256="a2be448869171b6e0f26d9544088b8b98439ec180ce272040236d570a40bcbed",
        url="https://pypi.org/packages/87/74/a4d55da28d7bba6d6f49430f22a62afd8472cb24a63fa61daef80d3e821b/testtools-2.3.0-py2.py3-none-any.whl",
    )
