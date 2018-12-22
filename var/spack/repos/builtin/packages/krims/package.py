# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Krims(CMakePackage):
    """The bucket of Krimskrams every C or C++ project needs"""

    homepage = "http://lazyten.org/krims"
    url      = "https://github.com/lazyten/krims/archive/v0.2.1.tar.gz"
    git      = "https://github.com/lazyten/krims.git"

    maintainers = ['mfherbst']

    #
    # Versions
    #
    version("develop", branch="master")
    version("0.2.1", "bf219656fd81c342a4782bad7d7beed0")

    #
    # Variants
    #
    # Library build type
    variant("build_type", default="DebugRelease",
            description="The build type to build",
            values=("Debug", "Release", "DebugRelease"))
    variant("shared", default=True,
            description="Build shared libraries (else the static one)")

    # Components
    variant("examples", default=False,
            description="Compile examples")

    #
    # Conflicts
    #
    # Only builds on clang > 3.5 and gcc > 4.8
    conflicts("%intel", msg="krims only builds with gcc and clang")
    conflicts("%gcc@:4.8")
    conflicts("%clang@:3.5")

    #
    # Dependencies
    #
    depends_on("cmake@3:", type="build")

    #
    # Settings and cmake cache
    #
    def cmake_args(self):
        spec = self.spec

        args = [
            "-DAUTOCHECKOUT_MISSING_REPOS=OFF",
            #
            "-DBUILD_SHARED_LIBS=" + str("+shared" in spec),
            "-DDRB_MACHINE_SPECIFIC_OPTIM_Release=ON",  # Adds -march=native
            #
            # TODO Hard-disable tests for now, since rapidcheck not in Spack
            "-DKRIMS_ENABLE_TESTS=OFF",
            "-DKRIMS_ENABLE_EXAMPLES=" + str("+examples" in spec),
        ]

        return args
