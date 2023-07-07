# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *


class Cpmd(AutotoolsPackage):
    """The CPMD code is a parallelized plane wave / pseudopotential
    implementation of Density Functional Theory, particularly designed
    for ab-initio molecular dynamics."""

    homepage = "https://github.com/CPMD-code"
    url = "https://github.com/CPMD-code/CPMD/archive/refs/tags/4.3.tar.gz"
    git = "https://github.com/CPMD-code/CPMD.git"
    maintainers = ["g-mathias"]

    version(
        "4.3",
        default=True,
        sha256="e0290f9da0d255f90a612e60662b14a97ca53003f89073c6af84fa7bc8739f65",
    )
    version("develop", branch="main")

    depends_on("blas")
    depends_on("lapack")

    variant("mpi", default=True, description="Enable MPI support")
    variant("debug", default=False, description="keep symbols for debugging")

    with when("+mpi"):
        depends_on("mpi@2:")
    variant("openmp", default=True, description="Enable OpenMP support")
    conflicts("^openblas threads=none", when="+openmp")
    conflicts("^openblas threads=pthreads", when="+openmp")
    extraflags = [
        "ALPHALINUX",
        "ALTIX",
        "BG",
        "CHECKS_IEEE_ARITHMETIC",
        "CUDA",
        "EREG",
        "ES",
        "FFT_HASNT_THREADED_COPIES",
        "FFT_HAS_LOW_LEVEL_TIMERS",
        "FFT_HAS_OMP_COLLAPSE",
        "FFT_HAS_SPECIAL_COPY",
        "HASNT_BF_STREAM_IO",
        "HASNT_F03_EXECUTE_COMMAND_LINE",
        "HASNT_F03_FEATURES",
        "HASNT_F03_ISO_FORTRAN_ENV",
        "HASNT_F08_ASYNCHRONOUS",
        "HASNT_F08_CONTIGUOUS",
        "HASNT_F08_ISO_FORTRAN_ENV",
        "HASNT_F08_POINTER_REMAPPING",
        "HASNT_MPI_30",
        "HASNT_MULTITHREAD_MPI_SUPPORT",
        "HASNT_OMP_45",
        "HASNT_OMP_COLLAPSE",
        "HASNT_OMP_SET_NESTED",
        "HAS_CUDA",
        "HAS_EXTERNAL_C_ERF",
        "HAS_EXTERNAL_IDAMIN",
        "HAS_EXTERNAL_IZAMAX",
        "HAS_IBM_QPX_INTRINSIC",
        "HAS_NVTX_TIMER",
        "HP",
        "HPC",
        "IBM",
        "NEC",
        "NOINT8",
        "NOMEMINFO",
        "NO_MEMSIZE",
        "OSX",
        "OSX_IFC",
        "PRIMEHPC",
        "PRIMERGY",
        "SGI",
        "SR11000",
        "SR11KIBM",
        "SR8000",
        "SUMFNL_ISNT_TRHEADED",
        "SUN",
        "USE_IBM_HPM",
        "VECTOR",
        "WINNT",
        "none",
    ]
    variant("eflags", values=extraflags, default="none", multi=True)
    # fft support
    variant(
        "fft",
        values=["default", "fftw3", "essl"],
        default="default",
        description="fft routines used",
    )
    with when("fft=fftw3"):
        depends_on("fftw-api@3")
    with when("fft=essl"):
        depends_on("essl")

    # libxc support
    variant("libxc", default=True, description="Support additional functionals via libxc")
    with when("+libxc"):
        depends_on("libxc@3:4.99", when="@4.3")
        depends_on("libxc@3:", when="@4.4:,develop")
        depends_on("pkgconfig", type="build")
    variant(
        "irat",
        default="2",
        values=["1", "2"],
        description="ratio bitlength float vs. int. Almost always 2 (64/32).",
    )
    variant("manual", default=False, description="build pdf and html manual")
    with when("+manual"):
        depends_on("texlive", type="build")

    def configure(self, spec, prefix):
        pkgconf = which("pkg-config")
        options = []
        fflags = []
        cflags = []
        cppflags = []
        lflags = []

        # process configure options
        if spec.satisfies("+openmp"):
            fflags.append(self.compiler.openmp_flag)
            cflags.append(self.compiler.openmp_flag)
        if spec.satisfies("+debug"):
            fflags.append("-g")
            cflags.append("-g")

        fft_flags = {
            "default": "-D__HAS_FFT_DEFAULT",
            "fftw3": "-D__HAS_FFT_FFTW3",
            "essl": "-D__HAS_FFT_ESSL",
        }
        cppflags.append(fft_flags[spec.variants["fft"].value])

        if spec.satisfies("+mpi"):
            cppflags.append("-D__PARALLEL")
        if spec.satisfies("fft=fftw3"):
            fflags.append(spec["fftw-api"].headers.cpp_flags)
            lflags.append(spec["fftw-api"].libs.ld_flags)
        if spec.satisfies("+libxc"):
            cppflags.append("-D__HAS_LIBXC")
            cppflags.extend(pkgconf("--cflags", "libxcf03", output=str).split())
            fflags.extend(pkgconf("--cflags-only-I", "libxcf03", output=str).split())
            lflags.extend(pkgconf("--libs", "libxcf03", "libxc", output=str).split())

        # BLAS & LAPACK
        lapack = spec["lapack"].libs
        blas = spec["blas"].libs
        lflags.append((lapack + blas).search_flags)
        lflags.append((lapack + blas).ld_flags)

        # compiler wisdom
        if spec.satisfies("%gcc@10:"):
            fflags.append("-fallow-argument-mismatch")
        for ef in spec.variants["eflags"].value:
            if ef != "none":
                cppflags.append("-D__{0}".format(ef))

        # write a minimal spack configuration
        cfg = "./configure/spack"
        with open(cfg, "a") as cfg_fh:
            cfg_fh.write("IRAT={0}\n".format(spec.variants["irat"].value))
            cfg_fh.write("CPP='/usr/bin/cpp -P -traditional'\n")
            cfg_fh.write("FFLAGS_GROMOS='$(FFLAGS) -fixed'\n")
            cfg_fh.write("FFLAGS_GROMOS_MODULES='$(FFLAGS)'\n")

        # setup environment
        env["FFLAGS"] = " ".join(fflags)
        env["CFLAGS"] = " ".join(cflags)
        env["CPPFLAGS"] = " ".join(cppflags)
        env["LFLAGS"] = " ".join(lflags)

        env["CC"] = spack_cc if "~mpi" in spec else spec["mpi"].mpicc
        env["FC"] = spack_fc if "~mpi" in spec else spec["mpi"].mpifc
        env["LD"] = spack_fc if "~mpi" in spec else spec["mpi"].mpifc

        # run cpmd configure script
        # needs bugfix in CPMD gitlab repo
        if spec.satisfies("@4.3"):
            os.chmod("./scripts/configure.sh", 0o755)
        configure = Executable("./configure.sh")
        options.append("spack")
        configure(*options)

    def build(self, spec, prefix):
        make()
        if spec.satisfies("+manual"):
            with working_dir(os.path.join("doc", "manual")):
                make("pdf")

    def install(self, spec, prefix):
        install_tree("bin", self.prefix.bin)
        install_tree("lib", self.prefix.lib)
        install("LICENSE", prefix.doc)
        install("README.md", prefix.doc)
        if spec.satisfies("+manual"):
            with working_dir(os.path.join("doc", "manual")):
                install("manual.pdf", prefix.doc)

    def test(self):
        test_dir = self.test_suite.current_test_data_dir
        test_file = join_path(test_dir, "1-h2o-pbc-geoopt.inp")
        opts = []
        if self.spec.satisfies("+mpi"):
            exe_name = self.spec["mpi"].prefix.bin.mpirun
            opts.extend(["-n", "2"])
            opts.append(join_path(self.prefix.bin, "cpmd.x"))
        else:
            exe_name = "cpmd.x"
        opts.append(test_file)
        opts.append(test_dir)
        expected = [
            "2       1        H        O              1.84444     0.97604",
            "3       1        H        O              1.84444     0.97604",
            "2   1   3         H     O     H              103.8663",
        ]
        self.run_test(exe_name, options=opts, expected=expected)
