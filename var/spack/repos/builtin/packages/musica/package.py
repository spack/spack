# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Musica(CMakePackage):
    """MUSICA - The multi-scale interface for chemistry and aerosols

    MUSICA is a software package which exposes a flexible
    API for including aerosol and gas-phase chemistry in
    many contexts across languages and platforms. It is designed to
    be used in conjunction with other software packages, such as
    climate models, to provide a comprehensive framework for
    simulating atmospheric chemistry processes.
    """

    homepage = "https://github.com/NCAR/musica"
    url = "https://github.com/NCAR/musica/archive/refs/tags/v0.10.1.tar.gz"
    git = "https://github.com/NCAR/musica.git"

    maintainers("kshores", "mattldawson", "boulderdaze")

    license("Apache-2.0", checked_by="kshores")

    # Versions
    version("0.10.1", sha256="edefab03a676a449761997734e6c5b654b2c4f92ce8f1cc66ef63b8ae8ccccf1")

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
