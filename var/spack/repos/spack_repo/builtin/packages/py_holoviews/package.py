# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyHoloviews(PythonPackage):
    """A Python library designed to make data analysis and visualization seamless and simple."""

    homepage = "https://holoviews.org/"
    pypi = "holoviews/holoviews-1.19.1.tar.gz"
    git = "https://github.com/holoviz/holoviews.git"

    maintainers("climbfuji")

    license("BSD-3-Clause", checked_by="climbfuji")

    version("1.20.2", sha256="8c78b798601ce3af31523667c6d1cb40df8d781249ebebbdb2c5f6143565e6d8")
    version("1.19.1", sha256="b9e85e8c07275a456c0ef8d06bc157d02b37eff66fb3602aa12f5c86f084865c")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-hatchling", type="build")
    depends_on("py-hatch-vcs", type="build")

    depends_on("py-bokeh@3.1:", type="run")
    depends_on("py-colorcet", type="run")
    depends_on("py-numpy@1.21:", type="run")
    depends_on("py-packaging", type="run")
    depends_on("py-pandas@1.3:", type="run")
    depends_on("py-panel@1:", type="run")
    depends_on("py-param@2", type="run")
    depends_on("py-pyviz-comms@2.1:", type="run")
