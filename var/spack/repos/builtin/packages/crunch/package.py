# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Crunch(CMakePackage):
    """Advanced DXTc texture compression and transcoding library."""

    homepage = "https://github.com/BinomialLLC/crunch"
    # Fork with CMake build system
    git = "https://github.com/rouault/crunch.git"

    # No stable releases since 2012
    version("master", branch="build_fixes")

    depends_on("cmake@3.5:", type="build")

    conflicts("platform=darwin")
