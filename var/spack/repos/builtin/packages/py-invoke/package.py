# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyInvoke(PythonPackage):
    """Pythonic task execution"""

    homepage = "https://www.pyinvoke.org/"
    pypi = "invoke/invoke-1.4.1.tar.gz"

    license("BSD-2-Clause")

    version(
        "1.4.1",
        sha256="87b3ef9d72a1667e104f89b159eaf8a514dbf2f3576885b2bbdefe74c3fb2132",
        url="https://pypi.org/packages/2c/16/f00efa99ae9f255142a230ce6819c37ae9dd29a7144477c1161cc72d01ed/invoke-1.4.1-py3-none-any.whl",
    )
    version(
        "1.2.0",
        sha256="4f4de934b15c2276caa4fbc5a3b8a61c0eb0b234f2be1780d2b793321995c2d6",
        url="https://pypi.org/packages/be/9f/8508712c9cad73ac0c8eeb2c3e51c9ef65136653dda2b512bde64109f023/invoke-1.2.0-py3-none-any.whl",
    )
