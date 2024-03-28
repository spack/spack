# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySnuggs(PythonPackage):
    """Snuggs are s-expressions for Numpy"""

    homepage = "https://github.com/mapbox/snuggs"
    url = "https://github.com/mapbox/snuggs/archive/1.4.1.zip"

    license("MIT")

    version(
        "1.4.1",
        sha256="ef38fd4400b96f3999c928396102e65d3b0aa2f22bbc2c5fa49e151608368487",
        url="https://pypi.org/packages/23/dd/f8a42549be3f02af7f1edd583b4b0a7e946e330aa2cef48a9bd2f43b87fa/snuggs-1.4.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-click", when="@1.1:1.4.2")
        depends_on("py-numpy", when="@1.1:")
        depends_on("py-pyparsing", when="@1.1:1.4.4")
