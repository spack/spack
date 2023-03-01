# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBluepyConfigfile(PythonPackage):
    """Python library for accessing BlueConfig`s"""

    homepage = "https://bbpgitlab.epfl.ch/nse/bluepy-configfile"
    git = "ssh://git@bbpgitlab.epfl.ch/nse/bluepy-configfile.git"

    version("develop", branch="main")
    version("0.1.19", tag="bluepy-configfile-v0.1.19")

    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-future@0.16:", type="run")
    depends_on("py-six@1.0:", type="run")
