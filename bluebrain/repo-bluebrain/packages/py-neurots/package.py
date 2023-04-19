# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNeurots(PythonPackage):
    """Python library for neuron synthesis"""

    homepage = "https://github.com/BlueBrain/NeuroTS"
    git = "https://github.com/BlueBrain/NeuroTS.git"

    version("develop", branch="main")
    version("3.3.1", tag="3.3.1")
    version("3.1.0", tag="3.1.0")  # Breaking change to use diameter-synthesis >= 0.4
    version("3.0.0", tag="3.0.0")  # First version of NeuroTS
    version("2.5.0", tag="2.5.0")  # Last version of TNS before renaming

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-diameter-synthesis@0.5.3:", type=("build", "run"), when="@3.3.1:")
    depends_on("py-matplotlib@1.3.1:", type=("build", "run"))
    depends_on("py-tmd@2.2.0:", type=("build", "run"))
    depends_on("py-morphio@3.0:3.999", type=("build", "run"))
    depends_on("py-neurom@3:3.999", type=("build", "run"))
    depends_on("py-scipy@1.6:", type=("build", "run"), when="@3.0.0:")
    depends_on("py-scipy@0.13.3:", type=("build", "run"), when="@:2.999")
    depends_on("py-numpy@1.15:1.21", type=("build", "run"), when="@:2.5.0")
    depends_on("py-numpy@1.22:", type=("build", "run"), when="@3.0.0:")
    depends_on("py-jsonschema@3.0.1:", type=("build", "run"))
