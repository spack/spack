##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Krims(CMakePackage):
    """The bucket of Krimskrams every C or C++ project needs"""

    maintainers = ['mfherbst']

    homepage = "http://lazyten.org/krims"
    url      = "https://github.com/lazyten/krims/archive/v0.2.1.tar.gz"

    version("0.2.1", "bf219656fd81c342a4782bad7d7beed0")
    version("develop", git="https://github.com/lazyten/krims.git",
            branch="master")

    variant("build_type", default="DebugRelease",
            description="The build type to build",
            values=("Debug", "Release", "DebugRelease"))
    variant("examples", default=False,
            description="Compile examples")

    # Build dependencies
    depends_on("cmake@3.0:", type="build")

    # Only builds on clang > 3.5 and gcc > 4.8
    conflicts("%intel", msg="krims only builds with gcc and clang")
    conflicts("%gcc@:4.8")
    conflicts("%clang@:3.5")

    def cmake_args(self):
        spec = self.spec

        args = [
            # TODO Always disable tests for now
            "-DKRIMS_ENABLE_TESTS=OFF",
            # TODO Only build shared libs for now
            "-DBUILD_SHARED_LIBS=ON",
            #
            "-DAUTOCHECKOUT_MISSING_REPOS=OFF",
            "-DDRB_MACHINE_SPECIFIC_OPTIM_Release=ON",  # Adds -march=native
        ]

        value = "ON" if "+examples" in spec else "OFF"
        args.append("-DKRIMS_ENABLE_EXAMPLES=" + value)

        return args
