# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXesmf(PythonPackage):
    """Universal Regridder for Geospatial Data."""

    homepage = "https://github.com/pangeo-data/xESMF"
    pypi = "xesmf/xesmf-0.8.4.tar.gz"

    license("MIT")

    version(
        "0.8.4",
        sha256="cf6a784f0065bf221caa352354e321a33b6683bca7ff41900fcf804ed46e94a1",
        url="https://pypi.org/packages/5f/f6/4bef5ac8adeea80a5438955ad341b657e2e24ae2a3f8f491c6876e7752e2/xesmf-0.8.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.7:0.8.2,0.8.4:")
        depends_on("py-cf-xarray@0.5.1:", when="@0.7:")
        depends_on("py-numba@0.55.2:", when="@0.7:")
        depends_on("py-numpy@1.16.0:", when="@0.7:")
        depends_on("py-shapely", when="@0.7:")
        depends_on("py-sparse@0.8:", when="@0.7:")
        depends_on("py-xarray@0.16.2:", when="@0.7:")
