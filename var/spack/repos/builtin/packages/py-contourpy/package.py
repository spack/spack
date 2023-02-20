# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyContourpy(PythonPackage):
    """Python library for calculating contours of 2D quadrilateral grids."""

    homepage = "https://github.com/contourpy/contourpy"
    pypi = "contourpy/contourpy-1.0.5.tar.gz"

    version("1.0.5", sha256="896631cd40222aef3697e4e51177d14c3709fda49d30983269d584f034acc8a4")

    depends_on("python@3.7:", type=("build", "link", "run"))
    depends_on("py-build", type="build")
    depends_on("py-pybind11@2.6:", type=("build", "link"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-numpy@1.16:", type=("build", "run"))
