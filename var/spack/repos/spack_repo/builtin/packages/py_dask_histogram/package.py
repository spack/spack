# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyDaskHistogram(PythonPackage):
    """Histograms with task scheduling."""

    homepage = "https://github.com/dask-contrib/dask-histogram"
    pypi = "dask_histogram/dask_histogram-2024.3.0.tar.gz"

    maintainers("wdconinc")

    license("BSD-3-Clause", checked_by="wdconinc")

    version("2025.2.0", sha256="ad59f787add2e280ccff409f36b8495d0a782689e6c9797b1d19fd95e3fde067")
    version("2024.12.1", sha256="cbb8c660c64eaed5c92d1987e9bad5287487548315befb00140caf90201b1641")
    version("2024.9.1", sha256="a3e778b606db4affcc4fc8b6d34f5d99e165ea1691da57f40659032cd79f03e8")
    version("2024.3.0", sha256="834d4d25f5e2c417f5e792fafaa55484c20c9f3812d175125de7ac34f994ef7b")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("python@3.9:", type=("build", "run"), when="@2025.2.0:")

    depends_on("py-hatchling@1.8:", type="build")
    depends_on("py-hatch-vcs", type="build")

    depends_on("py-boost-histogram@1.3.2:", type=("build", "run"))
    depends_on("py-dask@2021.03.0:", type=("build", "run"))
    depends_on("py-dask-awkward@2025:", type=("build", "run"), when="@2025.2.0:")
