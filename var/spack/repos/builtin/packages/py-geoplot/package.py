# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeoplot(PythonPackage):
    """geoplot is a high-level Python geospatial plotting library.

    It's an extension to cartopy and matplotlib which makes mapping easy:
    like seaborn for geospatial."""

    homepage = "https://github.com/ResidentMario/geoplot"
    pypi = "geoplot/geoplot-0.4.1.tar.gz"

    maintainers("adamjstewart")

    version(
        "0.4.1",
        sha256="3b7e6deefc397f5f9025f2cb625c57ad7826d7bc6a68270a853914a733e5cee2",
        url="https://pypi.org/packages/e1/8f/46133752e1f02e70501939e739b81cbc85c79d7398c963b8a25a3178bffe/geoplot-0.4.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-cartopy", when="@0.2.1:0.2.2,0.3:")
        depends_on("py-contextily@1.0.0:", when="@0.4.1:")
        depends_on("py-descartes", when="@0.3:0.4.1")
        depends_on("py-geopandas", when="@0.2.1:0.2.2,0.3:0.4.3")
        depends_on("py-mapclassify@2.1:", when="@0.4.1:")
        depends_on("py-matplotlib", when="@0.2.1:0.2.2,0.3:0.4")
        depends_on("py-pandas", when="@0.2.1:0.2.2,0.3:")
        depends_on("py-seaborn", when="@0.2.1:0.2.2,0.3:")
