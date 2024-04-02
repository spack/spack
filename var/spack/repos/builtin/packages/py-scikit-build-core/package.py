# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScikitBuildCore(PythonPackage):
    """scikit-build-core is a doubly improved build system generator
    for CPython C/C++/Fortran/Cython extensions. It features several
    improvements over the classic scikit-build build system generator."""

    homepage = "https://github.com/scikit-build/scikit-build-core"
    pypi = "scikit_build_core/scikit_build_core-0.2.0.tar.gz"
    git = "https://github.com/scikit-build/scikit-build-core"

    maintainers("wdconinc")

    license("Apache-2.0")

    version(
        "0.6.1",
        sha256="d9b4631f138ee8e75c203fdb75b3ef2dc6a66beb4fcfd47a3c68af82b4100db9",
        url="https://pypi.org/packages/4e/f3/7b19e4b6af177313b82e23b33bc2169f67bb7dd8c3ec47edd4d5d5ea1022/scikit_build_core-0.6.1-py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="680aa58988b589106d7297c6fa4cf55317aed726e3b5657bbb8a83514b04d2d0",
        url="https://pypi.org/packages/b3/24/1a76b509b7685c5a8cc835c7b3f44d961864fa48f1ae7d1b7a8932b16b71/scikit_build_core-0.6.0-py3-none-any.whl",
    )
    version(
        "0.2.0",
        sha256="ef25936c45f78b705983d7517dfc69450649f33a976f04c4e8253b6728e10d57",
        url="https://pypi.org/packages/16/d6/b144b3822e3eb8bae026487ab0b3e8588048d35fe13ad7efc825925dab84/scikit_build_core-0.2.0-py3-none-any.whl",
    )

    variant("pyproject", default=False, description="Enable pyproject.toml support")

    with default_args(type="run"):
        depends_on("python@3.7:")
        depends_on("py-exceptiongroup", when="^python@:3.10")
        depends_on("py-importlib-metadata", when="@0.3: ^python@:3.7")
        depends_on("py-importlib-resources@1.3:", when="@0.1.0-rc1: ^python@:3.8")
        depends_on("py-packaging@20.9:", when="@0.1.0-rc1:")
        depends_on("py-pathspec@0.10.1:", when="@0.1.0-rc1:+pyproject")
        depends_on("py-pyproject-metadata@0.5:", when="@0.1.0-rc1:+pyproject")
        depends_on("py-tomli@1.1:", when="@0.1.0-rc1: ^python@:3.10")
        depends_on("py-typing-extensions@3.10:", when="@0.1.0-rc1:0.7 ^python@:3.7")

    # Build system

    # Dependencies

    # Optional dependencies

    # Test dependencies
