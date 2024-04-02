# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAddict(PythonPackage):
    """addict is a Python module that gives you dictionaries
    whose values are both gettable and settable using
    attributes, in addition to standard item-syntax."""

    homepage = "https://github.com/mewwts/addict"
    url = "https://github.com/mewwts/addict/archive/v2.2.1.tar.gz"

    license("MIT")

    version(
        "2.2.1",
        sha256="1948c2a5d93ba6026eb91aef2c971234aaf72488a9c07ab8a7950f82ae30eea7",
        url="https://pypi.org/packages/14/6f/beb258220417c1a0fe11e842f2e012a1be7eeeaa72a1d10ba17a804da367/addict-2.2.1-py3-none-any.whl",
    )
