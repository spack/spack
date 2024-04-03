# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDunamai(PythonPackage):
    """Dynamic version generation."""

    homepage = "https://github.com/mtkennerly/dunamai"
    pypi = "dunamai/dunamai-1.13.1.tar.gz"

    license("MIT")

    version(
        "1.18.0",
        sha256="f9284a9f4048f0b809d11539896e78bde94c05b091b966a04a44ab4c48df03ce",
        url="https://pypi.org/packages/4f/7c/1f3e504c627c81f58b1e6120618266df3c1a52a6ee9170c6e3ab265376bc/dunamai-1.18.0-py3-none-any.whl",
    )
    version(
        "1.17.0",
        sha256="5aa4ac1085de10691269af021b10497261a5dd644f277e2a21822212604d877b",
        url="https://pypi.org/packages/15/8e/ab699ce8c856edada5c7b4b79188caa478406c4f5ed4be99d703ca2c6827/dunamai-1.17.0-py3-none-any.whl",
    )
    version(
        "1.13.1",
        sha256="f23d31fd3e7df1c16f018f4f0c408df7feda8cba9516f7c9822a29fa3ed665cd",
        url="https://pypi.org/packages/13/ed/cbc61cd53954bbdab845886b416a6343014710d0ef821e2a6aadc4b81f05/dunamai-1.13.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3", when="@:1.19.0")
        depends_on("py-importlib-metadata@1.6:", when="@1.8: ^python@:3.7")
        depends_on("py-packaging@20.9:", when="@1.7:")
