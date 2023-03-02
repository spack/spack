# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFzTdRecipe(PythonPackage):
    """Python package to read and modify the definitions and parameters used in circuit
    building."""

    homepage = "https://bbpteam.epfl.ch/documentation/projects/fz-td-recipe"
    git = "ssh://git@bbpgitlab.epfl.ch/hpc/circuit-building/fz-td-recipe.git"

    version("develop", branch="master")
    version("0.1.0.dev0", tag="fz-td-recipe-v0.1.0.dev0")

    depends_on("py-setuptools", type="build")

    depends_on("py-lxml", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
