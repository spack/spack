# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BigdftAtlab(AutotoolsPackage):
    """BigDFT-atlab: library for ATomic related operations."""

    homepage = "https://bigdft.org/"
    url = "https://gitlab.com/l_sim/bigdft-suite/-/archive/1.9.2/bigdft-suite-1.9.2.tar.gz"
    git = "https://gitlab.com/l_sim/bigdft-suite.git"

    version("develop", branch="devel")
    version("1.9.2", sha256="dc9e49b68f122a9886fa0ef09970f62e7ba21bb9ab1b86be9b7d7e22ed8fbe0f")
    version("1.9.1", sha256="3c334da26d2a201b572579fc1a7f8caad1cbf971e848a3e10d83bc4dc8c82e41")
    version("1.9.0", sha256="4500e505f5a29d213f678a91d00a10fef9dc00860ea4b3edf9280f33ed0d1ac8")

    variant("mpi", default=True, description="Enable MPI support")
    variant("openmp", default=True, description="Enable OpenMP support")
    variant("openbabel", default=False, description="Enable detection of openbabel compilation")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    depends_on("mpi", when="+mpi")
    depends_on("openbabel", when="+openbabel")

    for vers in ["1.9.0", "1.9.1", "1.9.2", "develop"]:
        depends_on("bigdft-futile@{0}".format(vers), when="@{0}".format(vers))

    configure_directory = "atlab"

    def configure_args(self):
        spec = self.spec
        prefix = self.prefix

        fcflags = []
        if "+openmp" in spec:
            fcflags.append(self.compiler.openmp_flag)

        if self.spec.satisfies("%gcc@10:"):
            fcflags.append("-fallow-argument-mismatch")

        args = [
            "FCFLAGS=%s" % " ".join(fcflags),
            "--with-futile-libs=%s" % spec["bigdft-futile"].libs.ld_flags,
            "--with-futile-incs=%s" % spec["bigdft-futile"].headers.include_flags + "/futile",
            "--with-moduledir=%s" % prefix.include,
            "--prefix=%s" % prefix,
            "--without-etsf-io",
        ]

        if "+mpi" in spec:
            args.append("CC=%s" % spec["mpi"].mpicc)
            args.append("CXX=%s" % spec["mpi"].mpicxx)
            args.append("FC=%s" % spec["mpi"].mpifc)
            args.append("F90=%s" % spec["mpi"].mpifc)
            args.append("F77=%s" % spec["mpi"].mpif77)
        else:
            args.append("--disable-mpi")

        if "+openmp" in spec:
            args.append("--with-openmp")
        else:
            args.append("--without-openmp")

        if "+openbabel" in spec:
            args.append("--enable-openbabel")
            args.append("--with-openbabel-libs=%s" % spec["openbabel"].prefix.lib)
            args.append("--with-openbabel-incs=%s" % spec["openbabel"].prefix.include)

        return args

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries("libatlab-*", root=self.prefix, shared=shared, recursive=True)
