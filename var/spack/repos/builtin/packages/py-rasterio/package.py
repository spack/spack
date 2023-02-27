# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRasterio(PythonPackage):
    """Rasterio reads and writes geospatial raster data.

    Geographic information systems use GeoTIFF and other formats to organize
    and store gridded, or raster, datasets. Rasterio reads and writes these
    formats and provides a Python API based on N-D arrays."""

    homepage = "https://github.com/rasterio/rasterio"
    pypi = "rasterio/rasterio-1.1.8.tar.gz"
    git = "https://github.com/rasterio/rasterio.git"

    maintainers("adamjstewart")

    version("master", branch="master")
    version("1.3.6", sha256="c8b90eb10e16102d1ab0334a7436185f295de1c07f0d197e206d1c005fc33905")
    version("1.3.5", sha256="92358c3d4d5d6f3c7cd2812c8832d5175abce02b11bc101ac9548ff07163e8e2")
    version("1.3.4", sha256="5a8771405276ecf00b8ee927bd0a81ec21778dcfc97e4a37d0b388f10c9a41a8")
    version("1.3.3", sha256="b6fb1f12489f3a678c05ddcb78a74f0b6f63836219f51c0541e505f5e5208e7d")
    version("1.3.2", sha256="a91b32f649bc5aa3259909349258eb7999b7e830375f63cd37ade2082066ec1c")
    version("1.3.1", sha256="91a22c512862e6411def675cd864eb63000ec2e0922c8bf25834c631ba80bdc1")
    version("1.3.0", sha256="90171035e5b201cdb85a9abd60181426366040d4ca44706958db982a030f8dc4")
    version("1.2.10", sha256="6062456047ba6494fe18bd0da98a383b6fad5306b16cd52a22e76c59172a2b5f")
    version("1.2.3", sha256="d8c345e01052b70ac3bbbe100c83def813c0ab19f7412c2c98e553d03720c1c5")
    version("1.1.8", sha256="f7cac7e2ecf65b4b1eb78c994c63bd429b67dc679b0bc0ecfe487d3d5bf88fd5")
    version("1.1.5", sha256="ebe75c71f9257c780615caaec8ef81fa4602702cf9290a65c213e1639284acc9")
    version("1.0.24", sha256="4839479621045211f66868ec49625979693450bc2e476f23e7e8ac4804eaf452")
    version("1.0a12", sha256="47d460326e04c64590ff56952271a184a6307f814efc34fb319c12e690585f3c")

    # From pyproject.toml
    depends_on("py-cython@0.29.29:", when="@1.3.3:", type="build")
    depends_on("py-cython@0.29.24:0.29", when="@1.3.0:1.3.2", type="build")

    # From setup.py
    depends_on("python@3.8:", when="@1.3:", type=("build", "link", "run"))
    depends_on("python@3.6:3.9", when="@1.2", type=("build", "link", "run"))
    depends_on("python@2.7:2.8,3.5:3.8", when="@1.1", type=("build", "link", "run"))
    depends_on("python@2.7:2.8,3.5:3.7", when="@:1.0", type=("build", "link", "run"))
    depends_on("py-affine", type=("build", "run"))
    depends_on("py-attrs", type=("build", "run"))
    depends_on("py-certifi", when="@1.2:", type=("build", "run"))
    depends_on("py-click@4:", when="@1.2.4:", type=("build", "run"))
    depends_on("py-click@4:7", when="@:1.2.3", type=("build", "run"))
    depends_on("py-cligj@0.5:", type=("build", "run"))
    depends_on("py-numpy@1.18:", when="@1.3:", type=("build", "link", "run"))
    depends_on("py-numpy@1.15:", when="@1.2:", type=("build", "link", "run"))
    depends_on("py-numpy", type=("build", "link", "run"))
    depends_on("py-snuggs@1.4.1:", type=("build", "run"))
    depends_on("py-click-plugins", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))

    # From README.rst and setup.py
    depends_on("gdal@3.1:", when="@1.3:")
    depends_on("gdal@2.4:3.3", when="@1.2.7:1.2")
    depends_on("gdal@2.3:3.2", when="@1.2.0:1.2.6")
    depends_on("gdal@1.11:3.2", when="@1.1.0:1.1")
    depends_on("gdal@1.11:3.0", when="@1.0.25:1.0")
    depends_on("gdal@1.11:2", when="@:1.0.24")
