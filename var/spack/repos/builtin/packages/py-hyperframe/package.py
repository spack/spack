# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHyperframe(PythonPackage):
    """HTTP/2 framing layer for Python"""

    homepage = "https://github.com/python-hyper/hyperframe/"
    pypi = "hyperframe/hyperframe-6.0.0.tar.gz"

    license("MIT")

    version(
        "6.0.0",
        sha256="a51026b1591cac726fc3d0b7994fbc7dc5efab861ef38503face2930fd7b2d34",
        url="https://pypi.org/packages/e7/38/ca89dce3bc19aa5d4d524a66b64ccc40e7bd4e39a80d9791e5e423e1fa1f/hyperframe-6.0.0-py3-none-any.whl",
    )
    version(
        "5.2.0",
        sha256="5187962cb16dcc078f23cb5a4b110098d546c3f41ff2d4038a9896893bbd0b40",
        url="https://pypi.org/packages/19/0c/bf88182bcb5dce3094e2f3e4fe20db28a9928cb7bd5b08024030e4b140db/hyperframe-5.2.0-py2.py3-none-any.whl",
    )
