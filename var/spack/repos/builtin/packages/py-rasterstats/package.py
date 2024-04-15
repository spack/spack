# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRasterstats(PythonPackage):
    """rasterstats is a Python module for summarizing geospatial raster datasets
    based on vector geometries. It includes functions for zonal statistics and
    interpolated point queries. The command-line interface allows for easy
    interperability with other GeoJSON tools."""

    homepage = "https://github.com/perrygeo/python-rasterstats"
    pypi = "rasterstats/rasterstats-0.17.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.17.0",
        sha256="b003bf9888c22d416d3af08deb288f7ea0e406a2c593ebc0386cbf96786e5195",
        url="https://pypi.org/packages/fd/f2/fb998f425aab6f3d2fbb574880349714c8756bd3a025186d9e8fe1aee8aa/rasterstats-0.17.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-affine", when="@0.14:0.18")
        depends_on("py-cligj@0.4:", when="@0.10:")
        depends_on("py-fiona", when="@0.10:0.17.0,0.19:")
        depends_on("py-numpy@1.9:", when="@0.10:")
        depends_on("py-rasterio@1.0.0:", when="@0.13:")
        depends_on("py-shapely", when="@0.10:")
        depends_on("py-simplejson", when="@0.11:")
