# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArchngv(PythonPackage):
    """Building workflow and circuit API for Neuro-Glia-Vascular circuits."""

    homepage = "https://bbpgitlab.epfl.ch/nse/ArchNGV"
    git = "ssh://git@bbpgitlab.epfl.ch/nse/ArchNGV.git"

    version("develop", branch="main")
    version("3.0.2", tag="ArchNGV-v3.0.2")

    depends_on("py-setuptools@42:", type="build")

    depends_on("py-numpy@1.19.5:1.22", type=("build", "run"))
    depends_on("py-scipy@1.5.0:", type=("build", "run"))
    depends_on("py-h5py@3.1.0:", type=("build", "run"))
    depends_on("py-libsonata@0.1.21:", type=("build", "run"))
    depends_on("py-bluepysnap@1.0.5:1", type=("build", "run"))
    depends_on("py-cached-property@1.5:", type=("build", "run"))
    depends_on("py-voxcell@3.0.0:", type=("build", "run"))
    depends_on("py-vascpy@0.1.0:", type=("build", "run"))
    depends_on("py-atlas-commons@0.1.4:", type=("build", "run"))

    depends_on("py-ngv-ctools@1.0:", type=("build", "run"))
    depends_on("spatial-index@2.0.0:", type=("build", "run"))
    depends_on("py-bluepy-configfile@0.1.11:", type=("build", "run"))
    depends_on("py-click@7.0:", type=("build", "run"))
    depends_on("py-numpy-stl@2.10:2.15.1", type=("build", "run"))
    depends_on("py-openmesh@1.1.2:", type=("build", "run"))
    depends_on("py-pyyaml@5.0:", type=("build", "run"))
    depends_on("py-pandas@1.1.0:", type=("build", "run"))
    depends_on("py-tess@0.3.2", type=("build", "run"))
    depends_on("py-morphio@3.3.1:", type=("build", "run"))
    depends_on("py-pytouchreader@1.4.7:", type=("build", "run"))
    depends_on("py-morph-tool@2.4.0:", type=("build", "run"))
    depends_on("snakemake@5.0:", type=("build", "run"))
    depends_on("py-tmd@2.0.11:", type=("build", "run"))
    depends_on("py-neurots@2.5.0", type=("build", "run"))
    depends_on("py-diameter-synthesis@0.2.5", type=("build", "run"))
    depends_on("py-trimesh@2.38.10:", type=("build", "run"))
    # needed for trimesh marchingcubes
    depends_on("py-scikit-image", type=("build", "run"))

    depends_on("py-dask+distributed@2.0:", type=("build", "run"))
    depends_on("py-distributed@2.0:", type=("build", "run"))
    depends_on("py-dask-mpi@2.0:", type=("build", "run"))

    depends_on("py-pytest", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests/unit")
