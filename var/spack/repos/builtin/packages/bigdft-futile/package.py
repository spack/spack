# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BigdftFutile(AutotoolsPackage, CudaPackage):
    """BigDFT-futile: a library handling most common FORTRAN low-level operations,
    like memory managment, profiling routines, I/O operations.
    It also supports yaml output and parsing for fortran programs.
    It also provides wrappers routines to MPI and linear algebra operations.
    This library is intensively used in BigDFT packages."""

    homepage = "https://bigdft.org/"
    url = "https://gitlab.com/l_sim/bigdft-suite/-/archive/1.9.2/bigdft-suite-1.9.2.tar.gz"
    git = "https://gitlab.com/l_sim/bigdft-suite.git"

    version("develop", branch="devel")
    version("1.9.2", sha256="dc9e49b68f122a9886fa0ef09970f62e7ba21bb9ab1b86be9b7d7e22ed8fbe0f")
    version("1.9.1", sha256="3c334da26d2a201b572579fc1a7f8caad1cbf971e848a3e10d83bc4dc8c82e41")
    version("1.9.0", sha256="4500e505f5a29d213f678a91d00a10fef9dc00860ea4b3edf9280f33ed0d1ac8")

    variant("mpi", default=True, description="Enable MPI support")
    variant("openmp", default=True, description="Enable OpenMP support")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    depends_on("python@3.0:", type=("build", "run"))

    depends_on("blas")
    depends_on("lapack")
    depends_on("libyaml")
    depends_on("py-pyyaml")
    depends_on("mpi", when="+mpi")

    configure_directory = "futile"

    def configure_args(self):
        spec = self.spec
        prefix = self.prefix

        linalg = [spec["blas"].libs.ld_flags, spec["lapack"].libs.ld_flags]

        python_version = spec["python"].version.up_to(2)
        pyyaml = join_path(spec["py-pyyaml"].prefix.lib, "python{0}".format(python_version))

        openmp_flag = []
        if "+openmp" in spec:
            openmp_flag.append(self.compiler.openmp_flag)

        args = [
            "FCFLAGS=%s" % " ".join(openmp_flag),
            "--with-ext-linalg=%s" % " ".join(linalg),
            "--with-yaml-path=%s" % spec["libyaml"].prefix,
            "--with-pyyaml-path=%s" % pyyaml,
            "--prefix=%s" % prefix,
        ]

        if "+openmp" in spec:
            args.append("--with-openmp")
        else:
            args.append("--without-openmp")

        if "+mpi" in spec:
            args.append("CC=%s" % spec["mpi"].mpicc)
            args.append("CXX=%s" % spec["mpi"].mpicxx)
            args.append("FC=%s" % spec["mpi"].mpifc)
            args.append("F90=%s" % spec["mpi"].mpifc)
            args.append("F77=%s" % spec["mpi"].mpif77)
        else:
            args.append("--disable-mpi")

        if "+cuda" in spec:
            args.append("--enable-opencl")
            args.append("--with-ocl-path=%s" % spec["cuda"].prefix)
            args.append("--enable-cuda-gpu")
            args.append("--with-cuda-path=%s" % spec["cuda"].prefix)

        return args

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries("libfutile-*", root=self.prefix, shared=shared, recursive=True)
