# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNumpyStl(PythonPackage):
    """Library to make reading, writing and modifying both binary and ascii STL files easy"""

    homepage = "https://github.com/WoLpH/numpy-stl/"
    pypi = "numpy-stl/numpy-stl-2.10.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "3.0.0",
        sha256="44d56dec3b409b73f7126089ece859d0213d302e39c2375496e64f6dc574347c",
        url="https://pypi.org/packages/02/ee/72e3df8eeedfb9cebc4c5c9038b3922084d0eaef1cc2b5ee81e555ee0451/numpy_stl-3.0.0-py3-none-any.whl",
    )
    version(
        "2.10.1",
        sha256="1c9f8209ba4fc9b5eb54740b375d6ab3c238ed3a1ce3f776d72e04f44c8b91fa",
        url="https://pypi.org/packages/c9/5d/6cf10be944702c8b4c49ee339790ef1b575607cbc3b1e2b3e8f993135458/numpy_stl-2.10.1-py2-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy", when="@2.17:")
        depends_on("py-python-utils@3.4.5:", when="@3:")
