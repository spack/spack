# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Cosimio(CMakePackage):
    """The CoSimIO is a small library for interprocess communication in
    CoSimulation contexts.  It is designed for exchanging data between
    different solvers or other software tools.  For performing coupled
    simulations it is used in combination with the CoSimulationApplication.
    It is implemented as a detached interface: it follows the interface of
    Kratos but is independent of it, which allows easy integration into
    other codes / solvers.
    """

    tags = ["fem", "finite-elements", "hpc", "cosimulation", "coupling"]

    homepage = "https://github.com/KratosMultiphysics/CoSimIO"
    git = "https://github.com/KratosMultiphysics/CoSimIO.git"
    url = "https://github.com/KratosMultiphysics/CoSimIO/archive/refs/tags/v4.3.0.tar.gz"

    maintainers("loumalouomega", "philbucher", "pooyan-dadvand")

    version("master", branch="master")
    version("4.3.0", sha256="108a8c0b042f0eb307984accaecb2b6fc1407afd0bd4b36a4c5a98470a757a66")
    version("4.2.0", sha256="0c7e96d689b016eefd86781c0a55ce2383088cd2612aadc9697a839a0fa8d2b3")
    version("4.1.0", sha256="de02c526835d021c851dbbc1f95e4c929b10d0daccbabc80bcdc7503343678fc")
    version("4.0.0", sha256="12f38d1282b41e1ebc1d2c66d799cb7537840495c98638c698215d390403f221")
    version("3.0.0", sha256="02c902c2b28ae71241c4faf33f3e7a44f363b1d9732c53363cd33ffbbbe81eea")

    # -------------------------------------------------------------------------
    # Variants
    # -------------------------------------------------------------------------
    variant("mpi", default=False, description="Enable MPI communication")
    variant("c", default=True, description="Build C API")
    variant("python", default=False, description="Build Python bindings")
    variant("fortran", default=False, description="Build Fortran API")
    variant("testing", default=False, description="Build tests")
    variant("strict", default=False, description="Enable strict compiler warnings")

    # -------------------------------------------------------------------------
    # Dependencies
    # -------------------------------------------------------------------------
    depends_on("cmake@3.15:", type="build")

    # MPI: any implementation satisfying the 'mpi' virtual package works
    # (e.g. openmpi, mpich, intel-oneapi-mpi, mvapich2, ...)
    depends_on("mpi", when="+mpi")

    # Python bindings
    depends_on("python@3.6:", when="+python", type=("build", "link", "run"))
    # pybind11 is vendored under external_libraries/ but the system copy is
    # preferred to avoid duplicating toolchain state.
    depends_on("py-pybind11", when="+python", type="build")

    extends("python", when="+python")

    # -------------------------------------------------------------------------
    # Build-environment setup
    # -------------------------------------------------------------------------
    def setup_build_environment(self, env):
        spec = self.spec
        if "+mpi" in spec:
            env.set("CC", spec["mpi"].mpicc)
            env.set("CXX", spec["mpi"].mpicxx)
            if "+fortran" in spec:
                env.set("FC", spec["mpi"].mpifc)

    # -------------------------------------------------------------------------
    # CMake arguments
    # -------------------------------------------------------------------------
    def cmake_args(self):
        # Spack already forwards CMAKE_BUILD_TYPE; only set CoSimIO-specific
        # knobs here so we don't override Spack's build-type logic.
        args = [
            self.define_from_variant("CO_SIM_IO_BUILD_C", "c"),
            self.define_from_variant("CO_SIM_IO_BUILD_PYTHON", "python"),
            self.define_from_variant("CO_SIM_IO_BUILD_FORTRAN", "fortran"),
            self.define_from_variant("CO_SIM_IO_BUILD_TESTING", "testing"),
            self.define_from_variant("CO_SIM_IO_BUILD_MPI", "mpi"),
            self.define_from_variant("CO_SIM_IO_STRICT_COMPILER", "strict"),
        ]
        return args

    # -------------------------------------------------------------------------
    # Linker flags - pull in libgfortran when using Fortran bindings with GCC
    # or Clang (which delegates Fortran compilation to gfortran).
    # -------------------------------------------------------------------------
    def flag_handler(self, name, flags):
        spec = self.spec
        if name == "ldflags":
            if "+fortran" in spec and spec.compiler.name in ["gcc", "clang", "apple-clang"]:
                fc = Executable(self.compiler.fc)
                libgfortran = fc(
                    "--print-file-name", "libgfortran." + dso_suffix, output=str
                ).strip()
                # If print-file-name echoed the bare name back, the shared
                # library was not found - fall back to the static archive.
                if libgfortran == "libgfortran." + dso_suffix:
                    libgfortran = fc("--print-file-name", "libgfortran.a", output=str).strip()
                # -L<libdir> -lgfortran is required on macOS
                # https://github.com/spack/spack/pull/25823#issuecomment-917231118
                flags.append("-L{0} -lgfortran".format(os.path.dirname(libgfortran)))
        return (flags, None, None)
