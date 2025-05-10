# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPyogrio(PythonPackage):
    """Vectorized spatial vector file format I/O using GDAL/OGR"""

    homepage = "https://pypi.org/project/pyogrio"
    pypi = "pyogrio/pyogrio-0.9.0.tar.gz"
    git = "https://github.com/geopandas/pyogrio.git"

    maintainers("climbfuji")

    license("MIT", checked_by="climbfuji")

    version("0.11.0", sha256="a7e0a97bc10c0d7204f6bf52e1b928cba0554c35a907c32b23065aed1ed97b3f")
    version("0.10.0", sha256="ec051cb568324de878828fae96379b71858933413e185148acb6c162851ab23c")
    version("0.9.0", sha256="6a6fa2e8cf95b3d4a7c0fac48bce6e5037579e28d3eb33b53349d6e11f15e5a8")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-wheel", type="build")
    depends_on("gdal@2.4:", type=("build", "link", "run"))
    depends_on("py-cython@0.29:", type="build")

    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.29:", type="build")
    # Strictly, this should be 0.28. However others in the dask ecosystem
    # require 0.29, which makes this fail to concretize. Since Versioneer 0.29 doesn't
    # break anything with 0.28, it should be safe to keep this aligned
    # https://github.com/python-versioneer/python-versioneer/releases/tag/0.29
    depends_on("py-versioneer@0.28: +toml", type="build")

    depends_on("gdal@2.4:", type=("build", "link", "run"))
    depends_on("py-certifi", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
