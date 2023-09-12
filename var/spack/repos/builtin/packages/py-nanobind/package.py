# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNanobind(PythonPackage):
    """nanobind -- Seamless operability between C++11 and Python.

    nanobind is a small binding library that exposes C++ types in
    Python and vice versa. It is reminiscent of Boost.Python and pybind11
    and uses near-identical syntax. In contrast to these existing tools,
    nanobind is more efficient: bindings compile in a shorter amount of time,
    produce smaller binaries, and have better runtime performance.
    """

    homepage = "https://nanobind.readthedocs.io"
    url = "https://github.com/wjakob/nanobind/archive/refs/tags/v1.2.0.tar.gz"
    git = "https://github.com/wjakob/nanobind.git"

    maintainers("ma595")

    version("master", branch="master", submodules=True)
    version(
        "1.4.0", tag="v1.4.0", commit="05cba0ef85ba2bb68aa115af4b74c30aa2aa7bec", submodules=True
    )
    version(
        "1.2.0", tag="v1.2.0", commit="ec9350b805d2fe568f65746fd69225eedc5e37ae", submodules=True
    )

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-scikit-build", type="build")

    depends_on("py-cmake@3.17:", type="build")
    depends_on("py-ninja", type="build")
