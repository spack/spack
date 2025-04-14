# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Latte(CMakePackage):
    """Open source density functional tight binding molecular dynamics."""

    homepage = "https://github.com/lanl/latte"
    url = "https://github.com/lanl/latte/tarball/v1.2.1"
    git = "https://github.com/lanl/latte.git"

    maintainers("jeanlucf22", "finkeljos")

    tags = ["ecp", "ecp-apps"]

    license("LGPL-2.0-or-later")

    version("master", branch="master")
    version("lattepy", branch="lattepy")
    version("1.2.2", sha256="ab1346939dbd70ffd89c5e5bf8d24946cb3655dc25b203bec7fc59c6c63e4c79")
    version("1.2.1", sha256="a21dda5ebdcefa56e9ff7296d74ef03f89c200d2e110a02af7a84612668bf702")
    version("1.0.1", sha256="67b2957639ad8e36b69bc6ea9a13085183a881562af9ca6d2b90b412ff073789")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated
    depends_on("cmake@3.1:", type="build")
    depends_on("blas")
    depends_on("lapack")

    variant("interface", default=False, description="Build with interfacing to use with sedacs")

    variant("mpi", default=True, description="Build with mpi")
    depends_on("mpi", when="+mpi")

    variant("progress", default=False, description="Use progress for fast solvers")
    depends_on("qmd-progress", when="+progress")

    variant("shared", default=True, description="Build shared libs")

    root_cmakelists_dir = "cmake"

    def cmake_args(self):
        options = []
        if self.spec.satisfies("+shared"):
            options.append("-DBUILD_SHARED_LIBS=ON")
        else:
            options.append("-DBUILD_SHARED_LIBS=OFF")
        if self.spec.satisfies("+mpi"):
            options.append("-DDO_MPI=ON")
            options.append("-DCMAKE_C_COMPILER=%s" % self.spec["mpi"].mpicc)
            options.append("-DCMAKE_CXX_COMPILER=%s" % self.spec["mpi"].mpicxx)
            options.append("-DCMAKE_Fortran_COMPILER=%s" % self.spec["mpi"].mpifc)
        if self.spec.satisfies("+progress"):
            options.append("-DPROGRESS=ON")

        if self.spec.satisfies("+interface"):
            options.append("-DMAKELIB=ON")

        # specify blas/lapack libs
        options.append("-DBLAS_LIBRARIES=%s" % self.spec["blas"].libs)
        options.append("-DLAPACK_LIBRARIES=%s" % self.spec["lapack"].libs)

        # flag needed to remove gfortran max line length constraint
        options.append("-DCMAKE_Fortran_FLAGS=-ffree-line-length-none")

        return options
