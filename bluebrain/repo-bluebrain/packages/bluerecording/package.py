# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bluerecording(PythonPackage):
    """Blue Brain SNAP is a Python library for accessing BlueBrain circuit models
    represented in SONATA format."""

    homepage = "https://bbpgitlab.epfl.ch/conn/personal/tharayil/bluerecording/"
    git = "https://bbpgitlab.epfl.ch/conn/personal/tharayil/bluerecording.git"
    url = "https://bbpgitlab.epfl.ch/conn/personal/tharayil/bluerecording/-/archive/0.0.3/bluerecording-0.0.3.tar.gz"

    version("develop", branch="main")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm", type="build")

    #depends_on("py-bluepysnap", type=("build", "run"))
    depends_on("py-mpi4py", type=("build", "run"))
    depends_on("py-h5py+mpi", type=("build", "run"))
    
    #depends_on("py-cached-property@1.0:", type=("build", "run"))
    #depends_on("py-h5py@3.0.1:3", type=("build", "run"))
    #depends_on("py-importlib-resources@5:", when="@2", type=("build", "run"))
    #depends_on("py-jsonschema@4", type=("build", "run"))
    #depends_on("py-libsonata@0.1.21:", type=("build", "run"))
    #depends_on("py-libsonata@0.1.24:", when="@2", type=("build", "run"))
    #depends_on("py-morphio@3", type=("build", "run"))
    #depends_on("py-morph-tool@2.4.3:2", type=("build", "run"))
    #depends_on("py-numpy@1.8:", type=("build", "run"))
    #depends_on("py-pandas@1.0.0:", type=("build", "run"))
    #depends_on("py-click@7.0:", type=("build", "run"))
    #depends_on("py-more-itertools@8.2.0:", type=("build", "run"))
    #depends_on("spatial-index@1.2.1:", type=("build", "run"))
