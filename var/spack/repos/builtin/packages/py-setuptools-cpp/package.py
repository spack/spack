# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySetuptoolsCpp(PythonPackage):
    """Simplified packaging for pybind11-based C++ extensions"""

    homepage = "https://github.com/dmontagu/setuptools-cpp"
    pypi = "setuptools_cpp/setuptools_cpp-0.1.0.tar.gz"

    maintainers("dorton")

    license("MIT")

    version(
        "0.1.0",
        sha256="cd8179c038a12dbf2914999928f193f54d4713fd11715efdc5d6f450f663c8bd",
        url="https://pypi.org/packages/fc/7a/aac83f37a6362d6693eb5f4cfbfc8d42d2253c2d4d7a0fcc2444368fdca2/setuptools_cpp-0.1.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3")
        depends_on("py-pybind11")
        depends_on("py-setuptools")
