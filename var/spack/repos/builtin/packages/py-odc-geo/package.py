# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOdcGeo(PythonPackage):
    """Geometry Classes and Operations (opendatacube)."""

    homepage = "https://github.com/opendatacube/odc-geo/"
    pypi = "odc-geo/odc-geo-0.1.2.tar.gz"

    license("Apache-2.0")

    version(
        "0.1.2",
        sha256="6f1d5bfb030ea9c1f21e16a8b5b3b1cb68b4d25f5e714fda767317b2bff69f97",
        url="https://pypi.org/packages/db/a8/136de018114e21fa7b78272e9d9ed80c30a1abac9351fa2ce99e1aa5e778/odc_geo-0.1.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.1.1-alpha1:")
        depends_on("py-affine")
        depends_on("py-cachetools")
        depends_on("py-numpy")
        depends_on("py-pyproj", when="@:0.3.0")
        depends_on("py-shapely")
