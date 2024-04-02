# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBinaryornot(PythonPackage):
    """Ultra-lightweight pure Python package to check if a file is binary or text."""

    homepage = "https://binaryornot.readthedocs.io"
    url = "https://github.com/audreyr/binaryornot/archive/0.4.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.4.4",
        sha256="b8b71173c917bddcd2c16070412e369c3ed7f0528926f70cac18a6c97fd563e4",
        url="https://pypi.org/packages/24/7e/f7b6f453e6481d1e233540262ccbfcf89adcd43606f44a028d7f5fae5eb2/binaryornot-0.4.4-py2.py3-none-any.whl",
    )
