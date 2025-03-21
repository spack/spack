# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NvplScalapack(Package):
    """NVPL ScaLAPACK (NVIDIA Performance Libraries ScaLAPACK)."""

    homepage = "https://docs.nvidia.com/nvpl/latest/scalapack/index.html"
    url = (
        "https://developer.download.nvidia.com/compute/nvpl/redist/nvpl_scalapack/"
        "linux-sbsa/nvpl_scalapack-linux-sbsa-0.2.1-archive.tar.xz"
    )

    maintainers("RMeli")

    version("0.2.1", sha256="dada4d1ecf044d90609b9e62750b383d11be9b22c87e109414bcc07dce3c83c9")

    provides("scalapack")

    variant("ilp64", default=False, description="Force 64-bit Fortran native integers")

    depends_on("nvpl-blas +ilp64", when="+ilp64")
    depends_on("nvpl-blas ~ilp64", when="~ilp64")
    depends_on("nvpl-lapack +ilp64", when="+ilp64")
    depends_on("nvpl-lapack ~ilp64", when="~ilp64")
    depends_on("mpi")

    requires("target=armv8.2a:", msg="Any CPU with Arm-v8.2a+ microarch")

    conflicts("%gcc@:7")
    conflicts("%clang@:13")

    def url_for_version(self, version):
        """Spack can't detect the version in the URL above"""
        url = "https://developer.download.nvidia.com/compute/nvpl/redist/nvpl_scalapack/linux-sbsa/nvpl_scalapack-linux-sbsa-{0}-archive.tar.xz"
        return url.format(version)

    @property
    def scalapack_headers(self):
        return find_all_headers(self.spec.prefix.include)

    @property
    def scalapack_libs(self):
        spec = self.spec

        int_type = "ilp64" if spec.satisfies("+ilp64") else "lp64"

        if any(
            spec.satisfies(f"^[virtuals=mpi] {mpi_library}")
            for mpi_library in ["mpich", "cray-mpich", "mvapich", "mvapich2"]
        ):
            mpi_type = "mpich"
        elif spec.satisfies("^[virtuals=mpi] openmpi"):
            mpi_type = "openmpi" + spec["openmpi"].version.up_to(1)
        else:
            raise InstallError(
                f"Unsupported MPI library {spec['mpi']}.\n"
                "Add support to the Spack package, if needed."
            )

        name = [f"libnvpl_blacs_{int_type}_{mpi_type}", f"libnvpl_scalapack_{int_type}"]

        return find_libraries(name, spec.prefix.lib, shared=True, recursive=True)

    def install(self, spec, prefix):
        install_tree(".", prefix)
