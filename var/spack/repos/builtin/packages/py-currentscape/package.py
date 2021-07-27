# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCurrentscape(PythonPackage):
    """Module to easily plot currentscape."""

    homepage = "https://bbpgitlab.epfl.ch/cells/currentscape"
    git = "git@bbpgitlab.epfl.ch:cells/currentscape.git"

    version("develop", branch="master")
    version("0.0.10", tag="currentscape-v0.0.10")
    version("0.0.9", tag="currentscape-v0.0.9")
    version("0.0.6", tag="currentscape-v0.0.6")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type="run")
    depends_on("py-matplotlib", type="run")
    depends_on("py-scipy", type="run")
    depends_on("py-bluepyopt", type="run")
    depends_on("py-palettable", type="run")
