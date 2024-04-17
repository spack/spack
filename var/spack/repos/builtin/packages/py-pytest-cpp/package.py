# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPytestCpp(PythonPackage):
    """Use pytest runner to discover and execute C++ tests."""

    homepage = "https://github.com/pytest-dev/pytest-cpp"
    pypi = "pytest-cpp/pytest-cpp-1.4.0.tar.gz"

    license("MIT")

    version(
        "1.5.0",
        sha256="b23784c1ad97ca5ee67c4513f04295263161daf14043783a61a955663f35934e",
        url="https://pypi.org/packages/35/58/40dac4487a7349a2e59b30d973a2651d5465244e0cb3e2ab6475d9b75826/pytest_cpp-1.5.0-py2.py3-none-any.whl",
    )
    version(
        "1.4.0",
        sha256="61dfb7d87042c8768a83d706750c3dbacb334d7bc994f6cf2b850af49225edfa",
        url="https://pypi.org/packages/cb/24/fc32d2397bb510a943b0bce5b1f68cc6e4b0053ef88f51c83213c8ae99e2/pytest_cpp-1.4.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-colorama")
        depends_on("py-pytest@:5.3,5.4.2:", when="@1.2.1:2.1")
