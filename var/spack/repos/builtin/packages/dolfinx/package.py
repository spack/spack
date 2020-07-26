# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dolfinx(CMakePackage):
    """Next generation FEniCS problem solving environment"""

    homepage = "https://github.com/FEniCS/dolfinx"
    url = "https://github.com/FEniCS/dolfinx/archive/master.zip"
    git = "https://github.com/FEniCS/dolfinx.git"

    version("master", branch="master")

    variant("doc", default=False, description="Builds the documentation")
    variant("kahip", default=False, description="kahip support")
    variant("parmetis", default=False, description="parmetis support")
    variant("slepc", default=False, description="slepc support")

    depends_on("cmake@3.9:", type="build")
    depends_on("pkgconfig")
    depends_on("mpi")
    depends_on("hdf5+hl+fortran")
    depends_on("boost")
    depends_on("eigen")
    depends_on("petsc+mpi+shared+hypre+metis")
    depends_on("scotch+mpi")

    depends_on("kahip", when="+kahip")
    depends_on("parmetis", when="+parmetis")
    depends_on("slepc", when="+slepc")

    depends_on("python@3.5:")
    depends_on("py-ufl")
    depends_on("py-ffcx")
    depends_on("py-fiat")
    depends_on("py-sphinx@1.0.1:", when="+doc", type="build")

    root_cmakelists_dir = "cpp"

    def cmake_args(self):
        return [
            "-DDOLFINX_SKIP_BUILD_TESTS=True",
            "-DDOLFINX_ENABLE_KAHIP=%s"%('ON' if "+kahip" in self.spec else 'OFF'),
            "-DDOLFINX_ENABLE_PARMETIS=%s"%('ON' if "+parmetis" in self.spec else 'OFF'),
            "-DDOLFINX_ENABLE_SLEPC=%s"%('ON' if "+slepc" in self.spec else 'OFF'),
        ]
