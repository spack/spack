# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPintXarray(PythonPackage):
    """A convenience wrapper for using pint with xarray"""

    homepage = "https://github.com/xarray-contrib/pint-xarray"
    pypi = "pint-xarray/pint-xarray-0.2.1.tar.gz"

    license("Apache-2.0")

    version(
        "0.3",
        sha256="a7d87c792a2e981cbff464bd1c875e872ef7a0c882a9395cfbc34512b3dcb1ab",
        url="https://pypi.org/packages/f2/2a/ca2d4ab154db0dc6f716e65a3c2d2f32a46e8ca8bd016962f517c779e57b/pint_xarray-0.3-py3-none-any.whl",
    )
    version(
        "0.2.1",
        sha256="ad51ecd1c8384f5d38b51d232d1f5f03061f47673ee215414cd0b59dc67329a7",
        url="https://pypi.org/packages/8d/d5/bb7c9b6e5e6489cefa1056146400d652df7abc227378e3fa5d089d214236/pint_xarray-0.2.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@0.3:")
        depends_on("python@3.7:", when="@0.2")
        depends_on("py-importlib-metadata", when="@:0.2 ^python@:3.7")
        depends_on("py-numpy@1.17.0:")
        depends_on("py-pint@0.16:", when="@0.2:")
        depends_on("py-xarray@0.16.1:", when="@0.2:")
