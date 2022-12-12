# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTrimesh(PythonPackage):
    """Import, export, process, analyze and view triangular meshes"""

    homepage = "https://github.com/mikedh/trimesh"
    pypi = "trimesh/trimesh-2.38.10.tar.gz"

    version(
        "3.17.1",
        sha256="025bb2fa3a2e87bdd6873f11db45a7ca19216f2f8b6aed29140fca57e32c298e",
        preferred=True,
    )
    version(
        "2.38.10",
        sha256="866e73ea35641ff2af73867c891d7f9b90c75ccb8a3c1e8e06e16ff9af1f8c64",
        preferred=True,
    )

    depends_on("py-setuptools", type="build")

    depends_on("py-networkx", type="run")
    depends_on("py-numpy", type="run")
    depends_on("py-shapely", type="run")
    depends_on("py-scipy", type="run")
    depends_on("py-svgpath", type="run")
    depends_on("py-lxml", type="run")
