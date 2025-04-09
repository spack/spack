# Copyright (C) 2024-2025 University Corporation for Atmospheric Research
#
# SPDX-License-Identifier: Apache-2.0

from spack.package import *


class Musica(CMakePackage):
    """MUSICA - The multi-scale interface for chemistry and aerosols

    MUSICA is a software package designed which exposes a flexible
    API for including aerosol and gas-phase chemistry in
    many contexts across languages and platforms. It is designed to
    be used in conjunction with other software packages, such as
    climate models, to provide a comprehensive framework for
    simulating atmospheric processes.
    """

    homepage = "https://github.com/NCAR/musica"
    git = "https://github.com/NCAR/musica"

    maintainers("kshores", "mattldawson", "boulderdaze")

    license("Apache-2.0", checked_by="kshores")

    # Versions
    version("0.10.1", tag="v0.10.1")

    # Options from CMake
    variant("mpi", default=False, description="Enable MPI support")
    variant("openmp", default=False, description="Enable OpenMP support")
    variant("tests", default=True, description="Enable tests")
    variant("fortran", default=False, description="Build Fortran interface")
    variant("micm", default=True, description="Enable MICM support")
    variant("tuvx", default=True, description="Enable TUV-x support")

    # Dependencies
    depends_on("cmake@3.21:", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
    depends_on("mpi", when="+mpi")

    def cmake_args(self):
        args = [
            self.define_from_variant("MUSICA_ENABLE_MPI", "mpi"),
            self.define_from_variant("MUSICA_ENABLE_OPENMP", "openmp"),
            self.define_from_variant("MUSICA_ENABLE_TESTS", "tests"),
            self.define_from_variant("MUSICA_BUILD_FORTRAN_INTERFACE", "fortran"),
            self.define_from_variant("MUSICA_ENABLE_MICM", "micm"),
            self.define_from_variant("MUSICA_ENABLE_TUVX", "tuvx"),
            self.define("MUSICA_ENABLE_INSTALL", True),
        ]
        return args

    def test(self):
        # This runs ctest in the install tree
        with working_dir(self.prefix):
            if "+tests" in self.spec:
                ctest("--output-on-failure")
