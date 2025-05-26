# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage
from spack.package import *


class PyDaskAwkward(PythonPackage):
    """Connecting awkward-array and Dask."""

    homepage = "https://github.com/dask-contrib/dask-awkward"
    pypi = "dask_awkward/dask_awkward-2025.5.0.tar.gz"

    maintainers("wdconinc")

    license("BSD-3-Clause", checked_by="wdconinc")

    version("2025.5.0", sha256="2e6e71562055b9b7eadaab5e66b23a78d23274487ebf38669bfd82e7346f3659")
    version("2024.12.2", sha256="13c5ef32c5489e9e32e9f9163eb13e045f722ed6ed0f17ce1e07f892fc77a547")

    variant("io", default=False, description="Add support for IO")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("python@3.9:", type=("build", "run"), when="@2025.3.0:")

    depends_on("py-hatchlingi@1.8.0:", type="build")
    depends_on("hatch-vcs", type="build")

    depends_on("py-awkward@2.5.1:", type=("build", "run"))
    depends_on("py-dask@2023.04:2025.3", type=("build", "run"))
    depends_on("py-cachetools", type=("build", "run"))
    depends_on("py-typing-extensions@4.8.0:", type=("build", "run"))

    depends_on("py-pyarrow", type=("build", "run"), when="+io")
