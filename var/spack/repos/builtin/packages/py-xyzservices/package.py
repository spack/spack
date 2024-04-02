# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXyzservices(PythonPackage):
    """xyzservices is a lightweight library providing a repository of
    available XYZ services offering raster basemap tiles."""

    homepage = "https://github.com/geopandas/xyzservices"
    pypi = "xyzservices/xyzservices-2023.10.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "2023.10.1",
        sha256="6a4c38d3a9f89d3e77153eff9414b36a8ee0850c9e8b85796fd1b2a85b8dfd68",
        url="https://pypi.org/packages/82/c3/e06dfa46464cce3eda4b86df8847cab99d9bc545c76807ee689545187a4c/xyzservices-2023.10.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@2023.5:")
