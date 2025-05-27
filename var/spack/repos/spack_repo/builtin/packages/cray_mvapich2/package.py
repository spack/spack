# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package
from spack_repo.builtin.packages.mpich.package import MpichEnvironmentModifications

from spack.package import *


class CrayMvapich2(MpichEnvironmentModifications, Package):
    """Cray/HPE packaging of MVAPICH2 for HPE Apollo systems"""

    homepage = "https://docs.nersc.gov/development/compilers/wrappers/"
    has_code = False  # Skip attempts to fetch source that is not available

    maintainers("hppritcha")

    version("8.1.0")
    version("8.0.16")
    version("8.0.14")
    version("8.0.11")
    version("8.0.9")
    version("7.7.16")
    version("7.7.15")
    version("7.7.14")
    version("7.7.13")

    provides("mpi@3")

    requires("platform=linux", msg="Cray MVAPICH2 is only available on Cray")

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        if self.spec.has_virtual_dependency("c"):
            env.set("MPICC", self["c"].cc)

        if self.spec.has_virtual_dependency("cxx"):
            env.set("MPICXX", self["cxx"].cxx)

        if self.spec.has_virtual_dependency("fortran"):
            env.set("MPIFC", self["fortran"].fortran)
            env.set("MPIF77", self["fortran"].fortran)

    def install(self, spec, prefix):
        raise InstallError(
            self.spec.format(
                "{name} is not installable, you need to specify "
                "it as an external package in packages.yaml"
            )
        )
