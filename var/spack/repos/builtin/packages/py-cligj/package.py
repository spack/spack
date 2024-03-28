# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCligj(PythonPackage):
    """Common arguments and options for GeoJSON processing commands, using Click."""

    homepage = "https://github.com/mapbox/cligj"
    pypi = "cligj/cligj-0.7.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.7.2",
        sha256="c1ca117dbce1fe20a5809dc96f01e1c2840f6dcc939b3ddbb1111bf330ba82df",
        url="https://pypi.org/packages/73/86/43fa9f15c5b9fb6e82620428827cd3c284aa933431405d1bcf5231ae3d3e/cligj-0.7.2-py3-none-any.whl",
    )
    version(
        "0.5.0",
        sha256="20f24ce9abfde3f758aec3399e6811b936b6772f360846c662c19bf5537b4f14",
        url="https://pypi.org/packages/e4/be/30a58b4b0733850280d01f8bd132591b4668ed5c7046761098d665ac2174/cligj-0.5.0-py3-none-any.whl",
    )
    version(
        "0.4.0",
        sha256="7588487f1afcefbe65ae477cdbd4fca1828a3000fc3332e165dacb1dcb005f8a",
        url="https://pypi.org/packages/e8/c1/d2a5a83f1bf59b820b5ffb0c63fc31d13279d7b985f260c1f8c5ca1693d0/cligj-0.4.0-py2-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-click@4:7", when="@0.5:0.7.1")
        depends_on("py-click@4:", when="@0.3:0.4,0.7.2:")
