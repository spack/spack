# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJamo(PythonPackage):
    """Python-jamo is a Python Hangul syllable decomposition
    and synthesis library for working with Hangul characters
    and jamo."""

    homepage = "https://github.com/jdongian/python-jamo"
    pypi = "jamo/jamo-0.4.1.tar.gz"

    license("Apache-2.0")

    version(
        "0.4.1",
        sha256="d4b94fd23324c606ed2fbc4037c603e2c3a7ae9390c05d3473aea1ccb6b1c3fb",
        url="https://pypi.org/packages/ac/cc/49812faae67f9a24be6ddaf58a2cf7e8c3cbfcf5b762d9414f7103d2ea2c/jamo-0.4.1-py3-none-any.whl",
    )
