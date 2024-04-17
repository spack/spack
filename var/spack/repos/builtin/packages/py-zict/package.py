# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyZict(PythonPackage):
    """Mutable mapping tools"""

    homepage = "https://zict.readthedocs.io/en/latest/"
    pypi = "zict/zict-1.0.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "3.0.0",
        sha256="5796e36bd0e0cc8cf0fbc1ace6a68912611c1dbd74750a3f3026b9b9d6a327ae",
        url="https://pypi.org/packages/80/ab/11a76c1e2126084fde2639514f24e6111b789b0bfa4fc6264a8975c7e1f1/zict-3.0.0-py2.py3-none-any.whl",
    )
    version(
        "1.0.0",
        sha256="be8c7a24e3e78f871b72bfff16245105d1f0448606b1decdae054a14bfdf5996",
        url="https://pypi.org/packages/64/b4/a904be4184814adb9dfc2e679c4e611392080a32726a657a34cab93b38c2/zict-1.0.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@3:")
        depends_on("py-heapdict", when="@0.0.3:2")
