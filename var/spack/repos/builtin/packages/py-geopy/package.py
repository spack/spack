# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeopy(PythonPackage):
    """geopy is a Python client for several popular geocoding web services."""

    homepage = "https://github.com/geopy/geopy"
    pypi = "geopy/geopy-2.1.0.tar.gz"

    maintainers("adamjstewart")

    license("MIT")

    version(
        "2.1.0",
        sha256="4db8a2b79a2b3358a7d020ea195be639251a831a1b429c0d1b20c9f00c67c788",
        url="https://pypi.org/packages/0c/67/915668d0e286caa21a1da82a85ffe3d20528ec7212777b43ccd027d94023/geopy-2.1.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-geographiclib@1.49:1", when="@:2.2")
