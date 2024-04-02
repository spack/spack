# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGriffe(PythonPackage):
    """Signatures for entire Python programs. Extract the structure, the frame,
    the skeleton of your project, to generate API documentation or find
    breaking changes in your API."""

    homepage = "https://mkdocstrings.github.io/griffe/"
    pypi = "griffe/griffe-0.22.0.tar.gz"

    license("ISC")

    version(
        "0.22.0",
        sha256="65c94cba634d6ad397c495b04ed5fd3f06d9b16c4f9f78bd63be9ea34d6b7113",
        url="https://pypi.org/packages/fe/ad/0b31357c29f9108c51e5ba85cdf989fe45652e4e24883da68be7e2272700/griffe-0.22.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@:0.30")
        depends_on("py-cached-property", when="@:0.30 ^python@:3.7")
