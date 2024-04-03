# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyUnyt(PythonPackage):
    """A package for handling numpy arrays with units."""

    homepage = "https://yt-project.org"
    pypi = "unyt/unyt-2.8.0.tar.gz"
    git = "https://github.com/yt-project/unyt.git"

    maintainers("charmoniumq")

    license("BSD-3-Clause")

    version(
        "2.9.2",
        sha256="77370720cb9edd898492bf5a735101c8eabac9d9a9259a43be25352007262b5d",
        url="https://pypi.org/packages/77/43/35fd177ee4d3353a0d42bb22214f492551548a51b97d4b9ed616c9936e39/unyt-2.9.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@:2")
        depends_on("py-numpy@1.17.5:", when="@:2")
        depends_on("py-sympy@1.5:", when="@:2")

    # Undocumented in 2.9.2

    # https://github.com/yt-project/unyt/blob/v2.9.2/setup.py#L50

    # https://github.com/yt-project/unyt/blob/v2.9.2/setup.py#L21
