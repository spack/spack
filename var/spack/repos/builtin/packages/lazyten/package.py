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
import os


class Lazyten(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    maintainers = ['mfherbst']

    homepage = "http://lazyten.org"
    url      = "https://github.com/lazyten/lazyten/archive/v0.4.1.tar.gz"

    version('0.4.1', 'd06f7996144e1bf1b0aee82c2af36e83')
    version("develop", git="https://github.com/lazyten/lazyten.git",
            branch="master")

    variant("build_type", default="DebugRelease",
            description="The build type to build",
            values=("Debug", "Release", "DebugRelease"))
    variant("examples", default=False,
            description="Compile examples")
    variant("arpack", default=True,
            description="Build with Arpack support")

    # Build dependencies
    depends_on("cmake@3.0:", type="build")

    # Only builds on clang > 3.5 and gcc > 4.8
    conflicts("%intel", msg="lazyten only builds with gcc and clang")
    conflicts("%gcc@:4.8")
    conflicts("%clang@:3.5")

    depends_on("krims@develop", when="@develop")
    depends_on("krims@0.2.1", when="@0.4.1")

    depends_on("blas")
    depends_on("lapack")
    depends_on("armadillo@4.000:")
    depends_on("arpack-ng", when="+arpack")

    def cmake_args(self):
        spec = self.spec

        args = [
            # TODO Always disable tests for now
            "-DLAZYTEN_ENABLE_TESTS=OFF",
            # TODO Only build shared libs for now
            "-DBUILD_SHARED_LIBS=ON",
            #
            "-DAUTOCHECKOUT_MISSING_REPOS=OFF",
            "-DDRB_MACHINE_SPECIFIC_OPTIM_Release=ON",  # Adds -march=native
        ]

        # Check if examples should be built.
        value = "ON" if "+examples" in spec else "OFF"
        args.append("-DLAZYTEN_ENABLE_EXAMPLES=" + value)

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
