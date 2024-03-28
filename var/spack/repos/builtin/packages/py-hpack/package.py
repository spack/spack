# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHpack(PythonPackage):
    """Pure-Python HPACK header compression"""

    homepage = "https://github.com/python-hyper/hpack"
    pypi = "hpack/hpack-4.0.0.tar.gz"

    license("MIT")

    version(
        "4.0.0",
        sha256="84a076fad3dc9a9f8063ccb8041ef100867b1878b25ef0ee63847a5d53818a6c",
        url="https://pypi.org/packages/d5/34/e8b383f35b77c402d28563d2b8f83159319b509bc5f760b15d60b0abf165/hpack-4.0.0-py3-none-any.whl",
    )
    version(
        "3.0.0",
        sha256="0edd79eda27a53ba5be2dfabf3b15780928a0dff6eb0c60a3d6767720e970c89",
        url="https://pypi.org/packages/8a/cc/e53517f4a1e13f74776ca93271caef378dadec14d71c61c949d759d3db69/hpack-3.0.0-py2.py3-none-any.whl",
    )
