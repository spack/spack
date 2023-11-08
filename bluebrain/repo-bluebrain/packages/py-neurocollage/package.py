# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNeurocollage(PythonPackage):
    """Python library to build and validate parameters of morphology synthesis."""

    homepage = "https://bbpgitlab.epfl.ch/neuromath/neurocollage"
    git = "ssh://git@bbpgitlab.epfl.ch/neuromath/neurocollage.git"

    version("develop", branch="main")
    version("0.3.2", tag="neurocollage-v0.3.2")

    depends_on("py-setuptools", type="build")

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("brainbuilder@0.17:", type=("build", "run"))
    depends_on("py-atlas-analysis@0.0.4:", type=("build", "run"))
    depends_on("py-bluepysnap@1:", type=("build", "run"))
    depends_on("py-click@8:", type=("build", "run"))
    depends_on("py-joblib@0.14:", type=("build", "run"))
    depends_on("py-matplotlib@3.4:", type=("build", "run"))
    depends_on("py-morph-tool@2.9:", type=("build", "run"))
    depends_on("py-neurom@3.2:", type=("build", "run"))
    depends_on("py-neurots@3.1.1:", type=("build", "run"))
    depends_on("py-numpy@1.23:", type=("build", "run"))
    depends_on("py-pandas@1.4:", type=("build", "run"))
    depends_on("py-pyglet@2:", type=("build", "run"))
    depends_on("py-pyquaternion@0.9.5:", type=("build", "run"))
    depends_on("py-region-grower@0.4:", type=("build", "run"))
    depends_on("py-scipy@1.8:", type=("build", "run"))
    depends_on("py-tqdm@4.60:", type=("build", "run"))
    depends_on("py-trimesh@3.6:3", type=("build", "run"))
    depends_on("py-voxcell@3.1.2:3", type=("build", "run"))
