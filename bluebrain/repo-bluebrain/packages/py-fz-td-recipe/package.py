# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFzTdRecipe(PythonPackage):
    """Python package to read and modify the definitions and parameters used in circuit
    building."""

    homepage = "https://github.com/BlueBrain/fz-td-recipe"
    git = "ssh://git@github.com/BlueBrain/fz-td-recipe.git"

    version("develop", branch="main")
    version("0.2.0", tag="fz-td-recipe-v0.2.0")
    version("0.1.2", tag="fz-td-recipe-v0.1.2")
    version("0.1.1", tag="fz-td-recipe-v0.1.1")
    version("0.1.0", tag="fz-td-recipe-v0.1.0")

    depends_on("py-setuptools", type="build", when="@:0.2")
    depends_on("py-hatchling", type="build", when="@0.2.1:")
    depends_on("py-hatch-vcs", type="build", when="@0.2.1:")

    depends_on("py-click", type=("build", "run"), when="@0.2:")
    depends_on("py-jsonschema", type=("build", "run"), when="@0.2:")
    depends_on("py-lxml@:4", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"), when="@0.1.2:")
    depends_on("py-pyyaml", type=("build", "run"), when="@0.2:")
