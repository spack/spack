# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBluepysnap(PythonPackage):
    """Blue Brain SNAP is a Python library for accessing BlueBrain circuit models
    represented in SONATA format."""

    homepage = "https://github.com/BlueBrain/snap"
    git = "https://github.com/BlueBrain/snap.git"
    pypi = "bluepysnap/bluepysnap-0.12.0.tar.gz"

    version("develop", branch="master")
    version("1.0.7", sha256="84f8dac041bad2e8f730089e6b20637c7af0435d8405d428434568cd7637e067")
    version("2.0.2", sha256="28e8584995cbff0be925f5296bd1385dd031d5262d8ab567ef7c0a6052256949")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-cached-property@1.0:", type=("build", "run"))
    depends_on("py-h5py@3.0.1:3", type=("build", "run"))
    depends_on("py-importlib-resources@5:", when="@2", type=("build", "run"))
    depends_on("py-jsonschema@4", type=("build", "run"))
    depends_on("py-libsonata@0.1.21:", type=("build", "run"))
    depends_on("py-libsonata@0.1.24:", when="@2", type=("build", "run"))
    depends_on("py-morphio@3", type=("build", "run"))
    depends_on("py-morph-tool@2.4.3:2", type=("build", "run"))
    depends_on("py-numpy@1.8:", type=("build", "run"))
    depends_on("py-pandas@1.0.0:", type=("build", "run"))
    depends_on("py-click@7.0:", type=("build", "run"))
    depends_on("py-more-itertools@8.2.0:", type=("build", "run"))
    depends_on("spatial-index@1.2.1:", type=("build", "run"))
