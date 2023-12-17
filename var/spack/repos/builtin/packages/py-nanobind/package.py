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

    maintainers("chrisrichardson", "garth-wells", "ma595")

    version("master", branch="master", submodules=True)
    version(
        "1.8.0", tag="v1.8.0", commit="1a309ba444a47e081dc6213d72345a2fbbd20795", submodules=True
    )
    version(
        "1.7.0", tag="v1.7.0", commit="555ec7595c89c60ce7cf53e803bc226dc4899abb", submodules=True
    )
    version(
        "1.6.2", tag="v1.6.2", commit="cc5ac7e61def198db2a8b65c6d630343987a9f1d", submodules=True
    )
    version(
        "1.5.2", tag="v1.5.2", commit="b0e24d5b0ab0d518317d6b263a257ae72d4d29a2", submodules=True
    )
    version(
        "1.5.1", tag="v1.5.1", commit="ec6168d06dbf2ab94c31858223bd1d7617222706", submodules=True
    )
    version(
        "1.5.0", tag="v1.5.0", commit="e85a51049db500383808aaa4a77306ff37d96131", submodules=True
    )
    version(
        "1.4.0", tag="v1.4.0", commit="05cba0ef85ba2bb68aa115af4b74c30aa2aa7bec", submodules=True
    )
    version(
        "1.2.0", tag="v1.2.0", commit="ec9350b805d2fe568f65746fd69225eedc5e37ae", submodules=True
    )

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-scikit-build", type="build")

    depends_on("cmake@3.17:", type="build")
    depends_on("ninja", type="build")

    @property
    def cmake_prefix_paths(self):
        paths = [join_path(self.prefix, self.spec["python"].package.platlib, "nanobind", "cmake")]
        return paths
