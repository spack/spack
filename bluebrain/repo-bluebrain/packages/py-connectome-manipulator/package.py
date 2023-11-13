# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyConnectomeManipulator(PythonPackage):
    """Connectome generator tool."""

    homepage = "https://bbpgitlab.epfl.ch/conn/structural/connectome_manipulator"
    git = "ssh://git@bbpgitlab.epfl.ch/conn/structural/connectome_manipulator.git"

    version("develop", branch="main")
    version("0.0.9", tag="connectome-manipulator-v0.0.9")
    version("0.0.8", tag="connectome-manipulator-v0.0.8")
    version("0.0.6", tag="connectome-manipulator-v0.0.6")
    version("0.0.4", tag="connectome-manipulator-v0.0.4")

    variant(
        "convert",
        default=False,
        description="Enable runtime support of converting output to SONATA",
    )

    depends_on("parquet-converters@0.8.0:", type="run", when="+convert")

    depends_on("py-bluepysnap@1.0.5:1", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-progressbar", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-voxcell", type=("build", "run"))
    depends_on("py-pyarrow+parquet@3.0.0:", type=("build", "run"))
    depends_on("py-jsonpickle", type=("build", "run"))
    depends_on("py-distributed", type=("build", "run"), when="@0.0.6:")
    depends_on("py-dask-mpi", type=("build", "run"), when="@0.0.6:")
    depends_on("py-tables", type=("build", "run"), when="@0.0.7:")

    depends_on("py-submitit", type=("build", "run"), when="@:0.0.4")
