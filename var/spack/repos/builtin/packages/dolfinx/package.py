# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dolfinx(CMakePackage):
    """Next generation FEniCS problem solving environment"""

    homepage = "https://github.com/FEniCS/dolfinx"
    git = "https://github.com/FEniCS/dolfinx.git"

    version("master", branch="master")

    variant("kahip", default=False, description="kahip support")
    variant("parmetis", default=False, description="parmetis support")
    variant("slepc", default=False, description="slepc support")

    variant("int64", default=False, description="use 64 bit integers for indexes")
    variant("complex", default=False, description="use complex numbers")

    depends_on("cmake@3.9:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("mpi")
    depends_on("hdf5+hl+fortran")
    depends_on("boost")
    depends_on("eigen")
    depends_on("petsc+mpi+shared+hypre+metis ~int64~complex", when="~int64~complex")
    depends_on("petsc+mpi+shared+hypre+metis +int64~complex", when="+int64~complex")
    depends_on("petsc+mpi+shared+hypre+metis ~int64+complex", when="~int64+complex")
    depends_on("petsc+mpi+shared+hypre+metis +int64+complex", when="+int64+complex")
    depends_on("scotch+mpi")

    depends_on("kahip", when="+kahip")
    depends_on("parmetis", when="+parmetis")
    depends_on("slepc", when="+slepc")

    depends_on("py-ffcx")

    root_cmakelists_dir = "cpp"

    def cmake_args(self):
        args = [
            "-DDOLFINX_SKIP_BUILD_TESTS=True",
            "-DDOLFINX_ENABLE_KAHIP=%s" % (
                'ON' if "+kahip" in self.spec else 'OFF'),
            "-DDOLFINX_ENABLE_PARMETIS=%s" % (
                'ON' if "+parmetis" in self.spec else 'OFF'),
            "-DDOLFINX_ENABLE_SLEPC=%s" % (
                'ON' if "+slepc" in self.spec else 'OFF'),
            "-DPython3_ROOT_DIR=%s" % self.spec['python'].home,
            "-DPython3_FIND_STRATEGY=LOCATION",
        ]

        if "platform=darwin" in self.spec:
            args += [
                "-DCMAKE_SKIP_BUILD_RPATH=FALSE",
                "-DCMAKE_BUILD_WITH_INSTALL_RPATH=TRUE",
                "-DCMAKE_INSTALL_RPATH=",
                "-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=TRUE",
            ]

        return args
