# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBluepyemodelnexus(PythonPackage):
    """Python library to optimize and evaluate electrical models (Nexus addon)."""

    homepage = "https://bbpgitlab.epfl.ch/cells/bluepyemodelnexus"
    git = "ssh://git@bbpgitlab.epfl.ch/cells/bluepyemodelnexus.git"

    version("0.0.3", tag="bluepyemodelnexus-v0.0.3")

    depends_on("py-setuptools", type="build")

    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-icselector", type=("build", "run"))
    depends_on("py-nexusforge@0.7.1:", type=("build", "run"))
    depends_on("py-entity-management@1.2:", type="run")
    depends_on("py-pyjwt@2.1.0:", type=("build", "run"))
    depends_on("py-bluepyemodel@0.0.57:", type=("build", "run"))
