# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDescartes(PythonPackage):
    """Use Shapely or GeoJSON-like geometric objects as matplotlib paths
    and patches"""

    pypi = "descartes/descartes-1.1.0.tar.gz"

    version(
        "1.1.0",
        sha256="4c62dc41109689d03e4b35de0a2bcbdeeb81047badc607c4415d5c753bd683af",
        url="https://pypi.org/packages/e5/b6/1ed2eb03989ae574584664985367ba70cd9cf8b32ee8cad0e8aaeac819f3/descartes-1.1.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-matplotlib", when="@1.1:")
