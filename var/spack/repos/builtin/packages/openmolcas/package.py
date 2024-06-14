# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class Openmolcas(CMakePackage):
    """OpenMolcas is a quantum chemistry software package.
    The key feature of OpenMolcas is the multiconfigurational approach to
    the electronic structure."""

    homepage = "https://gitlab.com/Molcas/OpenMolcas"
    url = "https://github.com/Molcas/OpenMolcas/archive/v19.11.tar.gz"

    license("LGPL-2.1-or-later")

    version("24.02", sha256="4184402c4ddd5c74905140a32c5a3f66d8682dc7736353ccd74522c7b7c5da02")
    version("23.06", sha256="31727161c15ea588217c6511a3007792c74c35391849fa0296c2288d836cf951")
    version("21.02", sha256="d0b9731a011562ff4740c0e67e48d9af74bf2a266601a38b37640f72190519ca")
    version("19.11", sha256="8ebd1dcce98fc3f554f96e54e34f1e8ad566c601196ee68153763b6c0a04c7b9")

    variant("mpi", default=False, description="Build with MPI support.")
    variant("openmp", default=False, description="Enable multi-threading.")
    variant("shared", default=True, description="Build dynamically-linked libraries.")
    variant("hdf5", default=True, description="Activate HDF5 support for wavefunction format.")
    variant("tests", default=False, description="Build the unit tests.")

    variant("fde", default=False, description="Enable Frozen-density-embedding (FDE) interface.")
    # variant("gromacs", default=False, description="Compile Gromacs interface.")
    # variant("block", default=False, description="Activate BLOCK-DMRG support.")
    # variant("chemps2", default=False, description="Activate CheMPS2-DMRG support.")
    # variant("dice", default=False, description="Activate Dice-SHCI support.")
    variant("tools", default=False, description="Compile supported tools.")

    # external projects
    variant("dmrg", default=False, description="Activate QCMaquis DMRG driver and library.")
    # variant("efplib", default=False, description="Enable EFPLib library for effective fragment potentials (requires External/efp submodule).")
    # variant("gen1int", default=False, description="Enable Gen1Int library for 1-electron integrals.")
    # variant("molgui", default=False, description="Enable the Molcas Graphical User Interface.")
    # variant("msym", default=False, description="Activate MSYM support (requires External/libmsym submodule).")
    # variant("neci", default=False, description="Activate NECI support (requires External/NECI submodule).")
    variant("nevpt2", default=False, description="Activate (DMRG)-NEVPT2 support.")
    # variant("wfa", default=False, description="Activate extended wavefunction analysis (requires External/libwfa submodule).")

    depends_on("cmake@3.12:", type="build")
    depends_on("hdf5+cxx", when="+hdf5")
    depends_on("lapack")
    depends_on("blas")
    for _pkg in ["openblas"] + list(INTEL_MATH_LIBRARIES):
        with when(f"^[virtuals=blas] {_pkg}"):
            depends_on(f"{_pkg}+ilp64 threads=openmp")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-pyparsing", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("mpi", when="+mpi")
    depends_on("globalarrays", when="+mpi")
    depends_on("libxc")

    depends_on("scine-qcmaquis+openmolcas", when="+dmrg")
    requires("+dmrg", when="+nevpt2")

    patch("CMakeLists.txt.patch", when="target=aarch64:")

    def setup_build_environment(self, env):
        env.set("MOLCAS", self.prefix)
        env.set("GAROOT", self.spec["globalarrays"].prefix)
        if "+dmrg" in self.spec:
            env.set("QCMaquis_ROOT", self.spec["scine-qcmaquis"].prefix)

    def setup_run_environment(self, env):
        env.set("MOLCAS", self.prefix)

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("OPENMP", "openmp"),
            self.define("GA_BUILD", False),
            self.define("EXTERNAL_LIBXC", self.spec["libxc"].prefix),
            self.define_from_variant("FDE", "fde"),
            # self.define_from_variant("GROMACS", "gromacs"),
            # self.define_from_variant("BLOCK", "block"),
            # self.define_from_variant("CHEMPS2", "chemps2"),
            # self.define_from_variant("DICE", "dice"),
            self.define_from_variant("HDF5", "hdf5"),
            self.define_from_variant("TOOLS", "tools"),
            self.define_from_variant("BUILD_TESTING", "tests"),
            self.define_from_variant("DMRG", "dmrg"),
            # self.define_from_variant("EFPLIB", "efplib"),
            # self.define_from_variant("GEN1INT", "gen1int"),
            # self.define_from_variant("MolGUI", "molgui"),
            # self.define_from_variant("MSYM", "msym"),
            # self.define_from_variant("NECI", "neci"),
            self.define_from_variant("NEVPT2", "nevpt2"),
            # self.define_from_variant("WFA", "wfa"),
        ]

        if self.spec["blas"].name == "openblas":
            args.extend(
                [
                    self.define("LINALG", "OpenBLAS"),
                    self.define("OPENBLASROOT", self.spec["openblas"].prefix),
                ]
            )
        elif self.spec["blas"].name in INTEL_MATH_LIBRARIES:
            args.append(self.define("LINALG", "MKL"))
        elif self.spec["blas"].name == "amdblis":
            args.append(self.define("LINALG", "AOCL"))

        if "+mpi" in self.spec:
            args.extend([self.define("MPI", True), self.define("GA", True)])

        return args
