# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVisualCortexAnalysis(PythonPackage):
    """Visual cortex analyses"""

    homepage = "https://bbpgitlab.epfl.ch/circuits/proj120/visual-cortex-analysis"
    git = "ssh://git@bbpgitlab.epfl.ch/circuits/proj120/visual-cortex-analysis.git"

    version("0.2.3", tag="visual-cortex-analysis-v0.2.3")

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("run"))
    depends_on("py-pandas", type=("run"))
    depends_on("py-lazy", type=("run"))
    depends_on("py-tqdm", type=("run"))
    depends_on("py-pyyaml", type=("run"))
    depends_on("py-seaborn", type=("run"))
    depends_on("py-frozendict", type=("run"))
    depends_on("py-bmtk", type=("run"))
    depends_on("py-mpi4py", type=("run"))
    depends_on("py-bbp-workflow", type=("run"))
