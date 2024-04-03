# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQuaternionic(PythonPackage):
    """Interpret numpy arrays as quaternionic arrays with numba acceleration"""

    homepage = "https://github.com/moble/quaternionic"
    pypi = "quaternionic/quaternionic-1.0.1.tar.gz"

    maintainers("nilsvu", "moble")

    license("MIT")

    version(
        "1.0.1",
        sha256="5e9ce1fa6a25d7339d3a9a9f4582b0244cbced21e289982c0fb2e0a54eabf491",
        url="https://pypi.org/packages/0c/fe/cc8eb0bccf084aa1cdeb777cd8adb5380e0a440ff98b4bb2dae653b6288c/quaternionic-1.0.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3.9", when="@0.3:1.0.1")
        depends_on("py-black@20.8-beta1:", when="@:1.0.1")
        depends_on("py-importlib-metadata@1:", when="@0.3.4:1.0.1 ^python@:3.7")
        depends_on("py-numba@0.50.0:", when="@:1.0.1")
        depends_on("py-numpy@1.13.0:1", when="@:1.0.1")
        depends_on("py-scipy@1.0.0:", when="@:1.0.6")
