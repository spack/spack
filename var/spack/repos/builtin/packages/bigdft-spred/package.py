# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BigdftSpred(AutotoolsPackage):
    """BigDFT-spred: a library for structure prediction tools,
    that is compiled on top of BigDFT routines."""

    homepage = "https://bigdft.org/"
    url = "https://gitlab.com/l_sim/bigdft-suite/-/archive/1.9.2/bigdft-suite-1.9.2.tar.gz"
    git = "https://gitlab.com/l_sim/bigdft-suite.git"

    version("develop", branch="devel")
    version("1.9.2", sha256="dc9e49b68f122a9886fa0ef09970f62e7ba21bb9ab1b86be9b7d7e22ed8fbe0f")
    version("1.9.1", sha256="3c334da26d2a201b572579fc1a7f8caad1cbf971e848a3e10d83bc4dc8c82e41")
    version("1.9.0", sha256="4500e505f5a29d213f678a91d00a10fef9dc00860ea4b3edf9280f33ed0d1ac8")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    variant("mpi", default=True, description="Enable MPI support")
    variant("openmp", default=True, description="Enable OpenMP support")
    variant("scalapack", default=True, description="Enable SCALAPACK support")

    depends_on("python@3.0:", type=("build", "run"))

    depends_on("blas")
    depends_on("lapack")
    depends_on("py-pyyaml")
    depends_on("mpi", when="+mpi")
    depends_on("scalapack", when="+scalapack")

    for vers in ["1.9.0", "1.9.1", "1.9.2", "develop"]:
        depends_on("bigdft-futile@{0}".format(vers), when="@{0}".format(vers))
        depends_on("bigdft-psolver@{0}".format(vers), when="@{0}".format(vers))
        depends_on("bigdft-core@{0}".format(vers), when="@{0}".format(vers))

    configure_directory = "spred"

    def configure_args(self):
        spec = self.spec
        prefix = self.prefix

        python_version = spec["python"].version.up_to(2)
        pyyaml = join_path(spec["py-pyyaml"].prefix.lib, "python{0}".format(python_version))

        openmp_flag = []
        if "+openmp" in spec:
            openmp_flag.append(self.compiler.openmp_flag)

        linalg = []
        if "+scalapack" in spec:
            linalg.append(spec["scalapack"].libs.ld_flags)
        linalg.append(spec["lapack"].libs.ld_flags)
        linalg.append(spec["blas"].libs.ld_flags)

        args = [
            "FCFLAGS=%s" % " ".join(openmp_flag),
            "--with-ext-linalg=%s" % " ".join(linalg),
            "--with-pyyaml-path=%s" % pyyaml,
            "--with-futile-libs=%s" % spec["bigdft-futile"].libs.ld_flags,
            "--with-futile-incs=%s" % spec["bigdft-futile"].headers.include_flags,
            "--with-psolver-libs=%s" % spec["bigdft-psolver"].prefix.lib,
            "--with-psolver-incs=%s" % spec["bigdft-psolver"].headers.include_flags,
            "--with-core-libs=%s" % spec["bigdft-core"].prefix.lib,
            "--with-core-incs=%s" % spec["bigdft-core"].headers.include_flags,
            "--with-moduledir=%s" % prefix.include,
            "--prefix=%s" % prefix,
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

        return args

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries("libspred-*", root=self.prefix, shared=shared, recursive=True)
