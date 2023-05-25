# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAtlasSplitter(PythonPackage):
    """CLI to split atlas regions and modify annotations accordingly"""

    homepage = "https://github.com/BlueBrain/atlas-splitter"
    git = "https://github.com/BlueBrain/atlas-splitter.git"
    pypi = "atlas-splitter/atlas-splitter-0.1.1.tar.gz"

    version("develop", branch="main")
    version("0.1.2", sha256="ad79132bc18eed0bfc2c5633adde274cb49161eb9e0f0ab4350807d7afdd7a2d")

    depends_on("py-atlas-commons@0.1.4:", type=("build", "run"))
    depends_on("py-pyarrow+parquet@8.0.0:", type=("build", "run"))
    depends_on("py-cgal-pybind@0.1.4:", type=("build", "run"))
    depends_on("py-click@7.0:", type=("build", "run"))
    depends_on("py-numpy@1.15.0:", type=("build", "run"))
    depends_on("py-pytest", type="test")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-voxcell@3.0.0:", type=("build", "run"))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests/test_app_layer_splitter.py")
