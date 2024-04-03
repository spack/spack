# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScikitBuild(PythonPackage):
    """scikit-build is an improved build system generator for CPython
    C/C++/Fortran/Cython extensions. It provides better support for
    additional compilers, build systems, cross compilation, and
    locating dependencies and their associated build requirements.

    The scikit-build package is fundamentally just glue between
    the setuptools Python module and CMake."""

    homepage = "https://scikit-build.readthedocs.io/en/latest/"
    pypi = "scikit-build/scikit_build-0.17.6.tar.gz"

    maintainers("coreyjadams")

    license("MIT")

    version(
        "0.17.6",
        sha256="18bd55e81841106eec93f30a297df4f301003791c41be46ef6428d58bd42d6b3",
        url="https://pypi.org/packages/fa/af/b3ef8fe0bb96bf7308e1f9d196fc069f0c75d9c74cfaad851e418cc704f4/scikit_build-0.17.6-py3-none-any.whl",
    )
    version(
        "0.15.0",
        sha256="14ae341652ac42eabd1e830bccfec9b2551a4d9c34329a5580591fdeb86b23a4",
        url="https://pypi.org/packages/e3/36/34551e5035757ba17582eb530402a16612ec0446f67f3c7d509f6e9d8e63/scikit_build-0.15.0-py2.py3-none-any.whl",
    )
    version(
        "0.12.0",
        sha256="60784b9c02b06ad263c673988ebb6faa269a2acc261bc4233a7cf7655c0213e0",
        url="https://pypi.org/packages/04/19/f694dbab665bc2aacaf614452b1577d740e5ce8518d1b10fced2522759bf/scikit_build-0.12.0-py2.py3-none-any.whl",
    )
    version(
        "0.11.1",
        sha256="dd236b60330f243e79a9795952c6efeb6e28fd0bd7a35fd92eb490456ae29356",
        url="https://pypi.org/packages/78/c9/7c2c7397ea64e36ebb292446896edcdecbb8c1aa6b9a1a32f6f67984c3df/scikit_build-0.11.1-py2.py3-none-any.whl",
    )
    version(
        "0.10.0",
        sha256="e343cd0f012e4cc282132324223a15e6bae23c77f9c3e7f3b3b067a0db08d3b2",
        url="https://pypi.org/packages/8a/b5/c6ca60421991c22e69b9a950b0d046e06d714f79f7071946ab885c7115fb/scikit_build-0.10.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.17:")
        depends_on("py-distro", when="@0.11:")
        depends_on("py-packaging", when="@0.7:")
        depends_on("py-setuptools@42:", when="@0.16:")
        depends_on("py-setuptools@28:", when="@0.5:0.15")
        depends_on("py-tomli", when="@0.17: ^python@:3.10")
        depends_on("py-typing-extensions@3.7:", when="@0.16: ^python@:3.7")
        depends_on("py-wheel@0.32:", when="@0.16:")
        depends_on("py-wheel@0.29:", when="@0.6:0.15")

    # Historical dependencies
