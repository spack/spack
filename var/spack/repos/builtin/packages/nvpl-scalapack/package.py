# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NvplScalapack(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url = "https://developer.download.nvidia.com/compute/nvpl/redist/nvpl_scalapack/" "linux-sbsa/nvpl_scalapack-linux-sbsa-0.0.0-archive.tar.xz"

    maintainers("RMeli")

    version("0.2.1", sha256="6655898327ed36afd0242719075447058c3c89640b5b9bbfeb5af4dd5c101174")

    variant("ilp64", default=False, description="Force 64-bit Fortran native integers")

    depends_on("nvpl-blas +ilp64", when="+ilp64")
    depends_on("nvpl-blas ~ilp64", when="~ilp64")
    depends_on("nvpl-lapack +ilp64", when="+ilp64")
    depends_on("nvpl-lapack ~ilp64", when="~ilp64")
    depends_on("mpi")

    provides("scalapack")

    requires("target=armv8.2a:", msg="Any CPU with Arm-v8.2a+ microarch")

    conflicts("%gcc@:7")
    conflicts("%clang@:13")

    @property
    def scalapack_headers(self):
        return find_all_headers(self.spec.prefix.include)

    @property
    def scalapack_libs(self):
        spec = self.spec

        if spec.satisfies("+ilp64"):
            int_type = "ilp64"
        else:
            int_type = "lp64"

        if any(spec.satisfies(mpi_library) for mpi_library in ["^mpich", "^cray-mpich", "^mvapich", "^mvapich2"]):
            mpi_type = "mpich"
        elif spec.satisfies("^openmpi"):
            mpi_type = "openmpi" + spec["openmpi"].version.up_to(1)

        name = [f"libnvpl_blacs_{int_type}_{mpi_type}", f"libnvpl_scalapack_{int_type}"]

        return find_libraries(name, spec.prefix.lib, shared=True, recursive=True)

    def install(self, spec, prefix):
        install_tree(".", prefix)
