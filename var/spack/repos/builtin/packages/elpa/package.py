# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *

#
# Please note that you can open issues on the github page of ELPA:
# https://github.com/marekandreas/elpa/issues
#


class Elpa(AutotoolsPackage, CudaPackage, ROCmPackage):
    """Eigenvalue solvers for Petaflop-Applications (ELPA)"""

    homepage = "https://elpa.mpcdf.mpg.de/"
    url = "https://elpa.mpcdf.mpg.de/software/tarball-archive/Releases/2015.11.001/elpa-2015.11.001.tar.gz"
    git = "https://gitlab.mpcdf.mpg.de/elpa/elpa.git"

    version("master", branch="master")

    version(
        "2022.11.001", sha256="75db3ac146f9a6a1598e3418ddcab2be2f40a30ef9ec4c00a3b5d3808c99c430"
    )
    version(
        "2022.11.001.rc2",
        sha256="13d67e7d69894c631b48e4fcac905b51c4e41554c7eb4731e98c4e205f0fab9f",
        deprecated=True,
    )
    version(
        "2021.11.001", sha256="fb361da6c59946661b73e51538d419028f763d7cb9dacf9d8cd5c9cd3fb7802f"
    )
    version(
        "2021.05.002_bugfix",
        sha256="deabc48de5b9e4b2f073d749d335c8f354a7ce4245b643a23b7951cd6c90224b",
    )
    version(
        "2021.05.001", sha256="a4f1a4e3964f2473a5f8177f2091a9da5c6b5ef9280b8272dfefcbc3aad44d41"
    )

    variant("openmp", default=True, description="Activates OpenMP support")
    variant("mpi", default=True, description="Activates MPI support")

    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")

    depends_on("blas")
    depends_on("lapack")
    depends_on("mpi", when="+mpi")
    depends_on("scalapack", when="+mpi")
    depends_on("rocblas", when="+rocm")
    depends_on("libtool", type="build")
    depends_on("python@3:", type="build")

    with when("@2021.11.01:"):
        variant(
            "autotune", default=False, description="Enables autotuning for matrix restribution"
        )
        depends_on("scalapack", when="+autotune")

    # fails to build due to broken type-bound procedures in OMP parallel regions
    conflicts(
        "+openmp",
        when="@2021.05.001: %gcc@:7",
        msg="ELPA-2021.05.001+ requires GCC-8+ for OpenMP support",
    )
    conflicts("+mpi", when="+rocm", msg="ROCm support and MPI are not yet compatible")

    def url_for_version(self, version):
        return "https://elpa.mpcdf.mpg.de/software/tarball-archive/Releases/{0}/elpa-{0}.tar.gz".format(
            str(version)
        )

    # override default implementation which returns static lib
    @property
    def libs(self):
        libname = "libelpa_openmp" if "+openmp" in self.spec else "libelpa"
        return find_libraries(libname, root=self.prefix, shared=True, recursive=True)

    @property
    def headers(self):
        suffix = "_openmp" if self.spec.satisfies("+openmp") else ""

        # upstream sometimes adds tarball suffixes not part of the internal version
        elpa_version = str(self.spec.version)
        for vsuffix in ("_bugfix",):
            if elpa_version.endswith(vsuffix):  # implementation of py3.9 removesuffix
                elpa_version = elpa_version[: -len(vsuffix)]

        incdir = os.path.join(
            self.spec.prefix.include,
            "elpa{suffix}-{version}".format(suffix=suffix, version=elpa_version),
        )

        hlist = find_all_headers(incdir)
        hlist.directories = [incdir]
        return hlist

    build_directory = "spack-build"
    parallel = False

    def configure_args(self):
        spec = self.spec
        options = []

        options += self.with_or_without("mpi")

        # TODO: --disable-sse-assembly, --enable-sparc64, --enable-neon-arch64
        # Don't include vsx; as of 2022.05 it fails (reported upstream).
        # Altivec SSE intrinsics are used anyway.
        simd_features = ["sse", "avx", "avx2", "avx512", "sve128", "sve256", "sve512"]

        for feature in simd_features:
            msg = "--enable-{0}" if feature in spec.target else "--disable-{0}"
            options.append(msg.format(feature))

        if spec.target.family != "x86_64":
            options.append("--disable-sse-assembly")

        if "%aocc" in spec:
            options.append("--disable-shared")
            options.append("--enable-static")

        # If no features are found, enable the generic ones
        if not any(f in spec.target for f in simd_features):
            options.append("--enable-generic")

        if self.compiler.name == "gcc":
            gcc_options = []
            gfortran_options = ["-ffree-line-length-none"]

            space_separator = " "
            options.extend(
                [
                    "CFLAGS=" + space_separator.join(gcc_options),
                    "FCFLAGS=" + space_separator.join(gfortran_options),
                ]
            )

        if "%aocc" in spec:
            options.extend(["FCFLAGS=-O3", "CFLAGS=-O3"])

        cuda_flag = "nvidia-gpu"
        if "+cuda" in spec:
            prefix = spec["cuda"].prefix
            options.append("--enable-{0}".format(cuda_flag))
            options.append("--with-cuda-path={0}".format(prefix))
            options.append("--with-cuda-sdk-path={0}".format(prefix))

            cuda_arch = spec.variants["cuda_arch"].value[0]

            if cuda_arch != "none":
                options.append(
                    "--with-{0}-compute-capability=sm_{1}".format(cuda_flag.upper(), cuda_arch)
                )
        else:
            options.append("--disable-{0}".format(cuda_flag))

        if "+rocm" in spec:
            options.append("--enable-amd-gpu")
            options.append("CXX={0}".format(self.spec["hip"].hipcc))
        elif "@2021.05.001:" in self.spec:
            options.append("--disable-amd-gpu")

        options += self.enable_or_disable("openmp")

        options += [
            "LDFLAGS={0}".format(spec["lapack"].libs.search_flags),
            "LIBS={0} {1}".format(spec["lapack"].libs.link_flags, spec["blas"].libs.link_flags),
        ]

        if "+mpi" in self.spec:
            options += [
                "CC={0}".format(spec["mpi"].mpicc),
                "CXX={0}".format(spec["mpi"].mpicxx),
                "FC={0}".format(spec["mpi"].mpifc),
                "SCALAPACK_LDFLAGS={0}".format(spec["scalapack"].libs.joined()),
            ]

        if "+autotune" in self.spec:
            options.append("--enable-autotune-redistribute-matrix")

        options.append("--disable-silent-rules")
        options.append("--without-threading-support-check-during-build")

        return options
