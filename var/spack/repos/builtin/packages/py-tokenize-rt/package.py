# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTokenizeRt(PythonPackage):
    """A wrapper around the stdlib `tokenize` which roundtrips."""

    homepage = "https://github.com/asottile/tokenize-rt"
    pypi = "tokenize_rt/tokenize_rt-4.2.1.tar.gz"

    license("MIT")

    version(
        "4.2.1",
        sha256="08a27fa032a81cf45e8858d0ac706004fcd523e8463415ddf1442be38e204ea8",
        url="https://pypi.org/packages/2f/e2/654a25ad594df2eb07f76e405f6f261d8fa9b5c06eb1e78549a086245455/tokenize_rt-4.2.1-py2.py3-none-any.whl",
    )
