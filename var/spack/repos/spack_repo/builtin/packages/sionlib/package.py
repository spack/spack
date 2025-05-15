# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Sionlib(AutotoolsPackage):
    """Scalable I/O library for parallel access to task-local files"""

    homepage = "https://www.fz-juelich.de/ias/jsc/EN/Expertise/Support/Software/SIONlib/_node.html"
    url = "https://apps.fz-juelich.de/jsc/sionlib/download.php?version=1.7.6"

    maintainers("pramodk")

    license("BSD-3-Clause")

    version(
        "1.7.6",
        sha256="e85253ed3cd17a3b1c124ccd704caea3ad3c200abfcca9cc0851cb14f5a60691",
        extension="tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")
    patch("for_aarch64.patch", when="target=aarch64:")

    def configure_args(self):
        args = []

        if self.spec.satisfies("^[virtuals=mpi] intel-oneapi-mpi"):
            args.append("--mpi=intel2")
        elif self.spec.satisfies("^[virtuals=mpi] mpich") or self.spec.satisfies(
            "^[virtuals=mpi] mvapich2"
        ):
            args.append("--mpi=mpich2")
        elif self.spec.satisfies("^[virtuals=mpi] openmpi"):
            args.append("--mpi=openmpi")

        return args
