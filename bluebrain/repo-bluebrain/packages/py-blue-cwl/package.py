# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBlueCwl(PythonPackage):
    """Pythonic Blue Brain Nexus access library."""

    homepage = "https://github.com/BlueBrain/blue-cwl"
    git = "https://github.com/BlueBrain/blue-cwl.git"
    pypi = "blue-cwl/blue_cwl-0.1.0.tar.gz"

    version("0.1.0", sha256="90df1c6ef97777df04a0a18b6871057878da891edb5ba1b0fa94610bfd27e2aa")

    depends_on("python@3.10:", type=("build", "run"))

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    # Bring in line with Spykfunc to load both module simultaneously (added `+dataset@3`)
    depends_on("py-pyarrow+dataset+parquet@3.0.0:", type=("build", "run"))
    depends_on("py-click@8.0.0:", type=("build", "run"))
    depends_on("py-voxcell", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-joblib", type=("build", "run"))

    depends_on("py-libsonata", type=("build", "run"))
    depends_on("py-entity-management@1.2.44:", type=("build", "run"))
    depends_on("py-fz-td-recipe", type=("build", "run"))
    depends_on("py-pydantic", type=("build", "run"))
    depends_on("py-morph-tool", type=("build", "run"))
    depends_on("py-jsonschema", type=("build", "run"))
    depends_on("py-luigi", type=("build", "run"))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests/unit")
