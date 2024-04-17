# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNpx(PythonPackage):
    """Some useful extensions for NumPy"""

    homepage = "https://github.com/nschloe/npx"
    pypi = "npx/npx-0.1.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.1.0",
        sha256="5e07deadbf43096d8e1ec63dcd51b34e8d638e8e7e4a95d465e143e5701a0308",
        url="https://pypi.org/packages/4b/c8/4d8f80bf78c38268274b29c45a1a99ade4ade02b4d8c444ddbcc5fbaf1dd/npx-0.1.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@0.0.17:0.0.20,0.0.23:")
        depends_on("py-numpy@1.20.0:", when="@0.0.17:")
