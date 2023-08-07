# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Additivefoam(Package):
    """AdditiveFOAM is a heat and mass transfer software for Additive Manufacturing (AM)"""

    homepage = "https://github.com/ORNL/AdditiveFOAM"
    git = "https://github.com/ORNL/AdditiveFOAM.git"
    url = "https://github.com/ORNL/AdditiveFOAM/archive/1.0.0.tar.gz"

    maintainers("streeve", "colemanjs", "gknapp1")

    tags = ["ecp"]

    version("main", branch="main")
    version("1.0.0", sha256="abbdf1b0230cd2f26f526be76e973f508978611f404fe8ec4ecdd7d5df88724c")

    depends_on("openfoam-org@10")
