# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BigdftPsolver(AutotoolsPackage, CudaPackage):
    """BigDFT-Psolver: a flexible real-space Poisson Solver based on
    Interpolating Scaling Functions. It constitutes a fundamental building block
    of BigDFT code, and it can also be used separately and linked to other codes."""

    homepage = "https://bigdft.org/"
    url = "https://gitlab.com/l_sim/bigdft-suite/-/archive/1.9.2/bigdft-suite-1.9.2.tar.gz"
    git = "https://gitlab.com/l_sim/bigdft-suite.git"

    version("develop", branch="devel")
    version("1.9.2", sha256="dc9e49b68f122a9886fa0ef09970f62e7ba21bb9ab1b86be9b7d7e22ed8fbe0f")
    version("1.9.1", sha256="3c334da26d2a201b572579fc1a7f8caad1cbf971e848a3e10d83bc4dc8c82e41")
    version("1.9.0", sha256="4500e505f5a29d213f678a91d00a10fef9dc00860ea4b3edf9280f33ed0d1ac8")

    variant("mpi", default=True, description="Enable MPI support")
    variant("openmp", default=True, description="Enable OpenMP support")
    variant("scalapack", default=True, description="Enable SCALAPACK support")
    variant(
        "shared", default=True, description="Build shared libraries"
    )  # Not default in bigdft, but is typically the default expectation

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    depends_on("python@3.0:", type=("build", "run"))

    depends_on("blas")
    depends_on("lapack")
    depends_on("py-pyyaml")
    depends_on("mpi", when="+mpi")
    depends_on("scalapack", when="+scalapack")

    for vers in ["1.9.0", "1.9.1", "1.9.2", "develop"]:
        depends_on(f"bigdft-futile@{vers}", when=f"@{vers}")
        depends_on(f"bigdft-atlab@{vers}", when=f"@{vers}")

    configure_directory = "psolver"

    def configure_args(self):
        spec = self.spec
        prefix = self.prefix

        python_version = spec["python"].version.up_to(2)
        pyyaml = join_path(spec["py-pyyaml"].prefix.lib, f"python{python_version}")

        openmp_flag = []
        if "+openmp" in spec:
            openmp_flag.append(self.compiler.openmp_flag)

        linalg = []
        if "+scalapack" in spec:
            linalg.append(spec["scalapack"].libs.ld_flags)
        linalg.append(spec["lapack"].libs.ld_flags)
        linalg.append(spec["blas"].libs.ld_flags)

        args = [
            f"FCFLAGS={' '.join(openmp_flag)}",
            f"--with-ext-linalg={' '.join(linalg)}",
            f"--with-pyyaml-path={pyyaml}",
            f"--with-futile-libs={spec['bigdft-futile'].libs.ld_flags}",
            f"--with-futile-incs={spec['bigdft-futile'].headers.include_flags}",
            f"--with-moduledir={prefix.include}",
            f"--prefix={prefix}",
            "--without-etsf-io",
        ]
        if spec.satisfies("+shared"):
            args.append("--enable-dynamic-libraries")

        if "+mpi" in spec:
            args.append(f"CC={spec['mpi'].mpicc}")
            args.append(f"CXX={spec['mpi'].mpicxx}")
            args.append(f"FC={spec['mpi'].mpifc}")
            args.append(f"F90={spec['mpi'].mpifc}")
            args.append(f"F77={spec['mpi'].mpif77}")
        else:
            args.append("--disable-mpi")

        if "+openmp" in spec:
            args.append("--with-openmp")
        else:
            args.append("--without-openmp")

        args.append(f"--with-atlab-libs={spec['bigdft-atlab'].prefix.lib}")

        if "+cuda" in spec:
            args.append("--enable-cuda-gpu")
            args.append(f"--with-cuda-path={spec['cuda'].prefix}")
            args.append(f"--with-cuda-libs={spec['cuda'].libs.link_flags}")

        return args

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries("libPSolver-*", root=self.prefix, shared=shared, recursive=True)
