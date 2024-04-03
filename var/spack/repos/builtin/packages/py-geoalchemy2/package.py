# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeoalchemy2(PythonPackage):
    """Using SQLAlchemy with Spatial Databases"""

    homepage = "https://geoalchemy-2.readthedocs.io/en/latest"
    pypi = "GeoAlchemy2/GeoAlchemy2-0.6.3.tar.gz"

    license("MIT")

    version(
        "0.6.3",
        sha256="0d1c9ea3ec13f6a522ccc3ffd2569ac524a6c6e80bab883e8805b28c48e77143",
        url="https://pypi.org/packages/49/4f/a10d1aed8211d42c9601a3977674fe03fc0bd5545944fd1cacd238532af2/GeoAlchemy2-0.6.3-py2.py3-none-any.whl",
    )
    version(
        "0.4.2",
        sha256="540be4d6f5e32b0f621b8b7cc7881682890fbf30f1304be9a533f7875c9b1776",
        url="https://pypi.org/packages/a9/78/3e17296bfda7e4b31e6353af8756c9748b57b441037408598cf287bae30e/GeoAlchemy2-0.4.2-py2.py3-none-any.whl",
    )

    variant("dev", default=False, description="Enable development dependencies")

    with default_args(type="run"):
        depends_on("py-sqlalchemy@0.8.0:", when="@0.2.6:0.8.4")
