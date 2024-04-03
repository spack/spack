# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyImagehash(PythonPackage):
    """A Python Perceptual Image Hashing Module"""

    homepage = "https://github.com/JohannesBuchner/imagehash"
    pypi = "ImageHash/ImageHash-4.3.1.tar.gz"

    maintainers("thomas-bouvier")

    license("BSD-2-Clause")

    version(
        "4.3.1",
        sha256="5ad9a5cde14fe255745a8245677293ac0d67f09c330986a351f34b614ba62fb5",
        url="https://pypi.org/packages/2d/b4/19a746a986c6e38595fa5947c028b1b8e287773dcad766e648897ad2a4cf/ImageHash-4.3.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy", when="@4.2:4.2.0,4.3:")
        depends_on("py-pillow", when="@4.2:4.2.0,4.3:")
        depends_on("py-pywavelets", when="@4.2:4.2.0,4.3:")
        depends_on("py-scipy", when="@4.2:4.2.0,4.3:")
