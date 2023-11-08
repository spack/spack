# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySynthesisWorkflow(PythonPackage):
    """Python library to build and validate parameters of morphology synthesis."""

    homepage = "https://bbpgitlab.epfl.ch/neuromath/synthesis-workflow"
    git = "ssh://git@bbpgitlab.epfl.ch/neuromath/synthesis-workflow.git"

    version("develop", branch="main")
    version("1.1.0", tag="synthesis-workflow-v1.1.0")

    depends_on("py-setuptools", type="build")

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("brainbuilder@0.18.3:", type=("build", "run"))
    depends_on("placement-algorithm@2.3.1", type=("build", "run"))
    depends_on("py-bluepy@2.5:", type=("build", "run"))
    depends_on("py-bluepy-configfile@0.1.19:", type=("build", "run"))
    depends_on("py-bluepymm@0.8.5:", type=("build", "run"))
    depends_on("py-bluepyparallel@0.2:", type=("build", "run"))
    depends_on("py-diameter-synthesis@0.5.3:", type=("build", "run"))
    depends_on("py-dictdiffer@0.9:", type=("build", "run"))
    depends_on("py-gitpython@3.1.30:", type=("build", "run"))
    depends_on("py-jinja2@3:", type=("build", "run"))
    depends_on("py-joblib@1.2:", type=("build", "run"))
    depends_on("py-jsonpath-ng@1.5.3:", type=("build", "run"))
    depends_on("py-luigi@3.2:", type=("build", "run"))
    depends_on("py-luigi-tools@0.2.1:", type=("build", "run"))
    depends_on("py-matplotlib@3.4:", type=("build", "run"))
    depends_on("py-morph-tool@2.9:", type=("build", "run"))
    depends_on("py-morphio@3.3.4:", type=("build", "run"))
    depends_on("py-neuroc@0.2.8:", type=("build", "run"))
    depends_on("py-neurocollage@0.3:", type=("build", "run"))
    depends_on("py-neurom@3.2.2:", type=("build", "run"))
    depends_on("py-neurots@3.3.1:", type=("build", "run"))
    depends_on("py-numpy@1.24.1:", type=("build", "run"))
    depends_on("py-pandas@1.5.3:", type=("build", "run"))
    depends_on("py-pyyaml@6:", type=("build", "run"))
    depends_on("py-region-grower@1:", type=("build", "run"))
    depends_on("py-scipy@1.10:", type=("build", "run"))
    depends_on("py-seaborn@0.12.2:", type=("build", "run"))
    depends_on("py-tmd@2.3.1:", type=("build", "run"))
    depends_on("py-tqdm@4.64.1:", type=("build", "run"))
    depends_on("py-voxcell@3.1.3:3", type=("build", "run"))
