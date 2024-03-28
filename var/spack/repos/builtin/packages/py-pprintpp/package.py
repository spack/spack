# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPprintpp(PythonPackage):
    """A drop-in replacement for pprint that's actually pretty"""

    homepage = "https://github.com/wolever/pprintpp"
    pypi = "pprintpp/pprintpp-0.4.0.tar.gz"

    version(
        "0.4.0",
        sha256="b6b4dcdd0c0c0d75e4d7b2f21a9e933e5b2ce62b26e1a54537f9651ae5a5c01d",
        url="https://pypi.org/packages/4e/d1/e4ed95fdd3ef13b78630280d9e9e240aeb65cc7c544ec57106149c3942fb/pprintpp-0.4.0-py2.py3-none-any.whl",
    )
