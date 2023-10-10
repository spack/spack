# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArchiveAdvisor(PythonPackage):
    """A tool to parse folders to log files that have to be deleted or checked before archival."""

    homepage = "https://bbpteam.epfl.ch/documentation/projects/archive-advisor"
    git = "ssh://git@bbpgitlab.epfl.ch/hpc/archive-advisor.git"

    version("develop", branch="main")
    version("0.0.6", tag="0.0.6")
    version("0.0.4", tag="0.0.4")
    version("0.0.3", tag="0.0.3")
    version("0.0.2", tag="0.0.2")
    version("0.0.1", tag="0.0.1")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-rich", type=("build", "run"))
    depends_on("py-gitpython", type=("build", "run"))
    depends_on("py-find-duplicate-files", type=("build", "run"))
