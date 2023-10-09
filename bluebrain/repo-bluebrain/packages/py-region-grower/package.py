# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRegionGrower(PythonPackage):
    """Python library for space-aware neuron synthesis."""

    homepage = "https://bbpgitlab.epfl.ch/neuromath/region-grower"
    git = "ssh://git@bbpgitlab.epfl.ch/neuromath/region-grower.git"

    version("develop", branch="main")
    version("1.2.2", tag="region-grower-v1.2.2")

    depends_on("py-setuptools", type="build")

    depends_on("python@3.9:", type=("build", "run"))

    depends_on("py-attrs@19.3.0:", type=("build", "run"))
    depends_on("py-click@8.0:", type=("build", "run"))
    depends_on("py-dask+dataframe+distributed@2023.3.2:", type=("build", "run"))
    depends_on("py-diameter-synthesis@0.5.4:", type=("build", "run"))
    depends_on("py-morphio@3.3.6:3", type=("build", "run"))
    depends_on("py-morph-tool@2.9.0:2 +neuron", type=("build", "run"))
    depends_on("py-neuroc@0.2.8:", type=("build", "run"))
    depends_on("py-neurom@3.0:3", type=("build", "run"))
    depends_on("py-neurots@3.4.2:3", type=("build", "run"))
    depends_on("py-pandas@1.5.3:", type=("build", "run"))
    depends_on("py-tqdm@4.28.1:", type=("build", "run"))
    depends_on("py-voxcell@3.1.1:3", type=("build", "run"))
    depends_on("py-dask-mpi@2022.4:", type=("build", "run"))
    depends_on("py-mpi4py@3.1.1:", type=("build", "run"))
