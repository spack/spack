# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rkcommon(CMakePackage):
    """
    This project represents a common set of C++ infrastructure and
    CMake utilities used by various components of Intel oneAPI
    Rendering Toolkit.
    """

    homepage = "https://github.com/ospray/rkcommon"
    git = "https://github.com/ospray/rkcommon.git"
    generator = "Ninja"

    version("1.9.0", tag="v1.9.0")

    depends_on("cmake@3.1:", type="build")
    depends_on("ninja", type="build")
    depends_on("tbb")
