##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
import os


class Lazyten(CMakePackage):
    """Lightweight linear algebra library based on lazy matrices"""

    homepage = "http://lazyten.org"
    url      = "https://github.com/lazyten/lazyten/archive/v0.4.1.tar.gz"
    git      = "https://github.com/lazyten/lazyten.git"

    maintainers = ['mfherbst']

    #
    # Versions
    #
    version("develop", branch="master")
    version('0.4.1', 'd06f7996144e1bf1b0aee82c2af36e83')

    #
    # Variants
    #
    # Library build type
    variant("build_type", default="DebugRelease",
            description="The build type to build",
            values=("Debug", "Release", "DebugRelease"))
    variant("shared", default=True,
            description="Build shared libraries (else the static one)")

    # Features
    variant("arpack", default=True,
            description="Build with Arpack support")

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

    depends_on("krims@develop", when="@develop")
    depends_on("krims@0.2.1",   when="@0.4.1")

    depends_on("blas")
    depends_on("lapack")
    depends_on("armadillo@4:")
    depends_on("arpack-ng",     when="+arpack")

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
            "-DLAZYTEN_ENABLE_TESTS=OFF",
            "-DLAZYTEN_ENABLE_EXAMPLES=" + str("+examples" in spec),
        ]

        # Tell lazyten where to look for the krims cmake config
        # and targets files
        krims_modules = os.path.join(spec["krims"].prefix.share, "cmake/krims")
        args.append("-Dkrims_DIR=" + krims_modules)

        # Add linear algebra backends
        lapack_blas = spec['lapack'].libs + spec['blas'].libs
        args.extend([
            "-DARMADILLO_INCLUDE_DIR=" + spec["armadillo"].prefix.include,
            "-DARMADILLO_LIBRARY=" + ";".join(spec["armadillo"].libs),
            #
            "-DLAPACK_FOUND=ON",
            "-DLAPACK_LIBRARIES=" + ";".join(lapack_blas),
        ])

        if "+arpack" in spec:
            args.append("-DARPACK_DIR=" + spec["arpack-ng"].prefix)
            args.append("-DARPACK_LIBRARY=" + ";".join(spec["arpack-ng"].libs))

        return args
