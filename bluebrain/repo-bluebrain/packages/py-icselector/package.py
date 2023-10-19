# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIcselector(PythonPackage):
    """Python library for ion channel model selection."""

    homepage = "https://bbpgitlab.epfl.ch/msg/icselector"
    git = "ssh://git@bbpgitlab.epfl.ch/msg/icselector.git"

    version("0.0.3", tag="v0.0.3")

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
