# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySvgutils(PythonPackage):
    """Python tools to create and manipulate SVG files."""

    homepage = "https://github.com/btel/svg_utils"
    pypi = "svgutils/svgutils-0.3.4.tar.gz"

    license("MIT")

    version(
        "0.3.4",
        sha256="4d08524a08126553c1a9bf2639616cf31290adea6fd235a3eb67d77c748abc00",
        url="https://pypi.org/packages/44/79/0367ebd8a2edfdc46332b90bce1fd183e25078ed1b0d446c6bf42ea7ba7a/svgutils-0.3.4-py3-none-any.whl",
    )
    version(
        "0.3.1",
        sha256="891bbc55c440b425f682ff5be3a9d55d6088b7bbf0db18824df5fb8f5058e59b",
        url="https://pypi.org/packages/81/af/0da722445643004b4adf09c3cff72d4902048072bc7237ae09e42a220388/svgutils-0.3.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-lxml", when="@0.1.4:0.1,0.3:")
