# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScikitBuildCore(PythonPackage):
    """scikit-build-core is a doubly improved build system generator
    for CPython C/C++/Fortran/Cython extensions. It features several
    improvements over the classic scikit-build build system generator."""

    homepage = "https://github.com/scikit-build/scikit-build-core"
    git = "https://github.com/scikit-build/scikit-build-core"
    pypi = "scikit-build-core/scikit_build_core-0.6.1.tar.gz"

    maintainers("wdconinc")

    version("0.6.1", sha256="392254a4ca7235c27a4be98cc24cd708f563171961ce37cff66120ebfda20b7a")
    version("0.6.0", sha256="1bea5ed83610b367f3446badd996f2356690548188d6d38e5b93152df311a7ae")
    version("0.5.1", sha256="c6dad5a5127b2abfaa23cb91d23ac21059fd77cddf7122b33fd07791024dcfbf")
    version("0.5.0", sha256="a42a95029b34b5cf892855342d9b9445c774cb797fcb24c8fc4c2fb42b18dfca")
    version("0.4.8", sha256="9fac1cac1a38ba1168190b7bd98f62aecf06cd46db7185ec8c27b27e0da4ad4b")
    version("0.4.7", sha256="fa53b045c0869005a21af6aa5f6c2bd70d0a1af93e8a098ea6ee1b47e3dea183")
    version("0.4.6", sha256="54f06b23dea20284730c437d6af4298299165950a55cb7fb933915e1070a35a1")
    version("0.4.5", sha256="99cef7978be1d7580f7c59f12023dcaefd79f57c7057957e02a91fd5ac1f4d2e")
    version("0.4.4", sha256="4494e36e9a59ee7060edefb87af9586915a3b6c5893ee0a928af5326abe13be5")
    version("0.4.3", sha256="7ecb2ea7510efc0696c5e6c15cd5640293b008e3642f358fb0b89aa729039cef")
    version("0.4.2", sha256="e262db6c86bb30c9dab3a9d541db257c767da8a71911ca61f8654ac9145d4d5c")
    version("0.4.1", sha256="5a5759139f742420cff1c0a11979213b5013f85bdbc2af82d14b11d623e322c0")
    version("0.4.0", sha256="d668a3855efe9710acb621f30bcb53f838a5e3b6c75db962e494795707707d1e")
    version("0.3.3", sha256="65d2d561c1a0f102825e72bdab036edf5a99255d05c3b5654c706607b6876d65")
    version("0.3.2", sha256="40dbdfca2ddc82c8936bcbe340e027337096f0fc41a1fea0b1856d0fda7259c8")
    version("0.3.1", sha256="a0cfb87f030454905622f79db2903e87057f458bbbc3cd64951c7a5ffb077f10")
    version("0.3.0", sha256="e28307605032245e342e773ac53bc3b841c01ea40ddef223cf82af30186384d9")
    version("0.2.2", sha256="4dca91c0c6a00a63bd287925f661f275c720c840dfebb71eea4ba551b456e2aa")
    version("0.2.1", sha256="80c89c9b982453b437aaf0ce950d28f7232ef259006f4854421952ee750aca57")
    version("0.2.0", sha256="d2a76d9447a412038dc5e25dd259b03c25278661a0c7c3da766bb971c1a9acd2")
    version("0.1.6", sha256="5aba721453a0abdd7839470d30a6586ebe5f58a65517dcef5784a36407d82def")
    version("0.1.5", sha256="3944bf40e6817740c306b0e4f1cdcbcc5acf56b545eb910940f4631ad9d49a35")
    version("0.1.4", sha256="7c0722cceffff6aee8a42222e5589b37392423ac5373c9b45e825cb2ff9d3525")
    version("0.1.3", sha256="aa4563edf4b6f8907c9a927bf3cbd3c388e10ff4c6b5900cb428819668db14cf")
    version("0.1.2", sha256="c1c714a49eea7820389a8c7b8abb67b53f3f6b9fdbdab899acd1ce9d9210eed9")
    version("0.1.1", sha256="6291bdfe27d1f3bc529c11b02478d8f28a7a0906004a95ab31392d4b18c62d87")
    version("0.1.0", sha256="3b51c88fb99d2cca488cc262fa659ad3d403e2a038f8ad1d87e5f36ff6cc8deb")

    variant("pyproject", default=False, description="Enable pyproject.toml support")

    depends_on("python@3.7:", type=("build", "run"))

    # Build system
    depends_on("py-hatchling", type="build")
    depends_on("py-hatch-vcs", type="build")

    # Dependencies
    depends_on("py-exceptiongroup", when="^python@:3.10", type=("build", "run"))
    depends_on("py-importlib-resources@1.3:", when="^python@:3.8", type=("build", "run"))
    depends_on("py-packaging@20.9:", type=("build", "run"))
    depends_on("py-tomli@1.1:", when="^python@:3.10", type=("build", "run"))
    depends_on("py-typing-extensions@3.10:", when="^python@:3.7", type=("build", "run"))
    depends_on("cmake@3.15:", type=("build", "run"))

    # Optional dependencies
    depends_on("py-pathspec@0.10.1:", when="+pyproject", type=("build", "run"))
    depends_on("py-pyproject-metadata@0.5:", when="+pyproject", type=("build", "run"))

    # Test dependencies
    depends_on("py-build +virtualenv", type="test")
    depends_on("py-cattrs@22.2:", type="test")
    depends_on("py-importlib-metadata", type=("build", "run"), when="@0.3: ^python@:3.7")
    depends_on("py-pathspec@0.10.1:", type="test")
    depends_on("py-pybind11", type="test")
    depends_on("py-pyproject-metadata@0.5:", type="test")
    depends_on("py-pytest@7:", type="test")
    depends_on("py-pytest-subprocess@1.5:", type="test")
    depends_on("py-setuptools", type="test")
    depends_on("py-wheel", type="test")


    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir("tests"):
            which("pytest")()
