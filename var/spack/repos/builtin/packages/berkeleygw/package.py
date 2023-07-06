# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Berkeleygw(MakefilePackage):
    """BerkeleyGW is a many-body perturbation theory code for excited states,
    using the GW method and the GW plus Bethe-Salpeter equation (GW-BSE) method
    to solve respectively for quasiparticle excitations and optical properties of
    materials."""

    homepage = "https://berkeleygw.org"

    maintainers("migueldiascosta")

    version(
        "3.0.1",
        sha256="7d8c2cc1ee679afb48efbdd676689d4d537226b50e13a049dbcb052aaaf3654f",
        url="https://berkeley.box.com/shared/static/m1dgnhiemo47lhxczrn6si71bwxoxor8.gz",
        expand=False,
    )
    version(
        "3.0",
        sha256="ab411acead5e979fd42b8d298dbb0a12ce152e7be9eee0bb87e9e5a06a638e2a",
        url="https://berkeley.box.com/shared/static/lp6hj4kxr459l5a6t05qfuzl2ucyo03q.gz",
        expand=False,
    )
    version(
        "2.1",
        sha256="31f3b643dd937350c3866338321d675d4a1b1f54c730b43ad74ae67e75a9e6f2",
        url="https://berkeley.box.com/shared/static/ze3azi5vlyw7hpwvl9i5f82kaiid6g0x.gz",
        expand=False,
    )

    # For parallel computing support, enable +mpi. It uses MPI and ScaLAPACK
    # which are inter-dependent in the berkeleygw code(they need each other):
    # https://github.com/spack/spack/pull/33948#issuecomment-1323805817
    variant("mpi", default=True, description="Build with MPI and ScaLAPACK support")
    variant("elpa", default=True, description="Build with ELPA support")
    variant("python", default=True, description="Build with Python support")
    variant("openmp", default=True, description="Build with OpenMP support")
    variant("hdf5", default=True, description="Builds with HDF5 support")
    variant("debug", default=False, description="Builds with DEBUG flag")
    variant("verbose", default=False, description="Builds with VERBOSE flag")

    depends_on("blas")
    depends_on("lapack")
    depends_on("mpi", when="+mpi")
    depends_on("scalapack", when="+mpi")
    depends_on("hdf5+fortran+hl", when="+hdf5~mpi")
    depends_on("hdf5+fortran+hl+mpi", when="+hdf5+mpi")
    depends_on("elpa+openmp", when="+elpa+openmp")
    depends_on("elpa~openmp", when="+elpa~openmp")
    depends_on("fftw-api@3+openmp", when="+openmp")
    depends_on("fftw-api@3~openmp", when="~openmp")

    # in order to run the installed python scripts
    depends_on("python", type=("build", "run"), when="+python")
    depends_on("py-numpy", type=("build", "run"), when="+python")
    depends_on("py-setuptools", type=("build", "run"), when="+python")
    depends_on("py-h5py", type=("build", "run"), when="+hdf5+python")

    depends_on("perl", type="test")

    conflicts("+elpa", when="~mpi", msg="elpa is a parallel library and needs MPI support")

    # Force openmp propagation on some providers of blas / fftw-api
    with when("+openmp"):
        depends_on("fftw+openmp", when="^fftw")
        depends_on("amdfftw+openmp", when="^amdfftw")
        depends_on("openblas threads=openmp", when="^openblas")
        depends_on("amdblis threads=openmp", when="^amdblis")

    parallel = False

    def edit(self, spec, prefix):
        # archive is a tar file, despite the .gz expension
        tar = which("tar")
        tar("-x", "-f", self.stage.archive_file, "--strip-components=1")

        # get generic arch.mk template
        if "+mpi" in spec:
            copy(join_path(self.stage.source_path, "config", "generic.mpi.linux.mk"), "arch.mk")
        else:
            copy(join_path(self.stage.source_path, "config", "generic.serial.linux.mk"), "arch.mk")

        if self.version == Version("2.1"):
            # don't try to install missing file
            filter_file("install manual.html", "#install manual.html", "Makefile")

        # don't rebuild in the install and test steps
        filter_file("install: all", "install:", "Makefile")
        filter_file("check: all", "check:", "Makefile")

        # use parallelization in tests
        filter_file(
            r"cd testsuite \&\& \$\(MAKE\) check$",
            "cd testsuite && export BGW_TEST_MPI_NPROCS=2 OMP_NUM_THREADS=2 \
             SAVETESTDIRS=yes TEMPDIRPATH=%s && \
             $(MAKE) check-parallel"
            % join_path(self.build_directory, "tmp"),
            "Makefile",
        )

        # remove stack ulimit in order to run openmp tests
        filter_file(
            r"function run_testsuite\(\) {",
            "function run_testsuite() {\nulimit -s unlimited",
            "testsuite/run_testsuite.sh",
        )

        # slightly raise tolerance of some tests
        si_epm_tests = ["Si", "Si_cplx_spin"]
        if self.version >= Version("3.0"):
            si_epm_tests.append("Si_hdf5")
        for test in si_epm_tests:
            filter_file(
                "Precision : 6e-15",
                "Precision : 7e-15",
                join_path("testsuite", "Si-EPM", test + ".test"),
            )
        for test in ["Si_subspace", "Si_subspace_cplx", "Si_subspace_cplx_spin"]:
            filter_file(
                "Precision : 6e-15",
                "Precision : 7e-15",
                join_path("testsuite", "Si-EPM_subspace", test + ".test"),
            )
        filter_file("Precision : 8e-15", "Precision : 9e-15", "testsuite/GaAs-EPM/GaAs.test")

    def build(self, spec, prefix):
        buildopts = []
        paraflags = []

        if "+mpi" in spec:
            paraflags.append("-DMPI")

        # We need to copy fflags in case we append to it (#34019):
        fflags = spec.compiler_flags["fflags"][:]
        if "+openmp" in spec:
            paraflags.append("-DOMP")
            fflags.append(self.compiler.openmp_flag)

        if "+mpi" in spec:
            buildopts.append("C_PARAFLAG=-DPARA")
            buildopts.append("PARAFLAG=%s" % " ".join(paraflags))

        debugflag = ""
        if "+debug" in spec:
            debugflag += "-DDEBUG "
        if "+verbose" in spec:
            debugflag += "-DVERBOSE "
        buildopts.append("DEBUGFLAG=%s" % debugflag)

        if "+mpi" in spec:
            buildopts.append("LINK=%s" % spec["mpi"].mpifc)
            buildopts.append("C_LINK=%s" % spec["mpi"].mpicxx)
        else:
            buildopts.append("LINK=%s" % spack_fc)
            buildopts.append("C_LINK=%s" % spack_cxx)

        buildopts.append("FOPTS=%s" % " ".join(fflags))
        buildopts.append("C_OPTS=%s" % " ".join(spec.compiler_flags["cflags"]))

        mathflags = []

        mathflags.append("-DUSEFFTW3")
        buildopts.append("FFTWINCLUDE=%s" % spec["fftw-api"].prefix.include)
        fftwspec = spec["fftw-api:openmp" if "+openmp" in spec else "fftw-api"]
        buildopts.append("FFTWLIB=%s" % fftwspec.libs.ld_flags)

        buildopts.append("LAPACKLIB=%s" % spec["lapack"].libs.ld_flags)

        if "+mpi" in spec:
            mathflags.append("-DUSESCALAPACK")
            buildopts.append("SCALAPACKLIB=%s" % spec["scalapack"].libs.ld_flags)

        if spec.satisfies("%intel"):
            buildopts.append("COMPFLAG=-DINTEL")
            buildopts.append("MOD_OPT=-module ")
            buildopts.append("FCPP=cpp -C -P -ffreestanding")
            if "+mpi" in spec:
                buildopts.append("F90free=%s -free" % spec["mpi"].mpifc)
                buildopts.append("C_COMP=%s" % spec["mpi"].mpicc)
                buildopts.append("CC_COMP=%s" % spec["mpi"].mpicxx)
                buildopts.append("BLACSDIR=%s" % spec["scalapack"].libs)
                buildopts.append("BLACS=%s" % spec["scalapack"].libs.ld_flags)
            else:
                buildopts.append("F90free=%s -free" % spack_fc)
                buildopts.append("C_COMP=%s" % spack_cc)
                buildopts.append("CC_COMP=%s" % spack_cxx)
            buildopts.append("FOPTS=%s" % " ".join(fflags))
        elif spec.satisfies("%gcc"):
            c_flags = "-std=c99"
            cxx_flags = "-std=c++0x"
            f90_flags = "-ffree-form -ffree-line-length-none -fno-second-underscore"
            if spec.satisfies("%gcc@10:"):
                c_flags += " -fcommon"
                cxx_flags += " -fcommon"
                f90_flags += " -fallow-argument-mismatch"
            buildopts.append("COMPFLAG=-DGNU")
            buildopts.append("MOD_OPT=-J ")
            buildopts.append("FCPP=cpp -C -nostdinc")
            if "+mpi" in spec:
                buildopts.append("F90free=%s %s" % (spec["mpi"].mpifc, f90_flags))
                buildopts.append("C_COMP=%s %s" % (spec["mpi"].mpicc, c_flags))
                buildopts.append("CC_COMP=%s %s" % (spec["mpi"].mpicxx, cxx_flags))
            else:
                buildopts.append("F90free=%s %s" % (spack_fc, f90_flags))
                buildopts.append("C_COMP=%s %s" % (spack_cc, c_flags))
                buildopts.append("CC_COMP=%s %s" % (spack_cxx, cxx_flags))
            buildopts.append("FOPTS=%s" % " ".join(fflags))
        elif spec.satisfies("%fj"):
            c_flags = "-std=c99"
            cxx_flags = "-std=c++0x"
            f90_flags = "-Free"
            buildopts.append("COMPFLAG=")
            buildopts.append("MOD_OPT=-module ")
            buildopts.append("FCPP=cpp -C -nostdinc")
            if "+mpi" in spec:
                buildopts.append("F90free=%s %s" % (spec["mpi"].mpifc, f90_flags))
                buildopts.append("C_COMP=%s %s" % (spec["mpi"].mpicc, c_flags))
                buildopts.append("CC_COMP=%s %s" % (spec["mpi"].mpicxx, cxx_flags))
            else:
                buildopts.append("F90free=%s %s" % (spack_fc, f90_flags))
                buildopts.append("C_COMP=%s %s" % (spack_cc, c_flags))
                buildopts.append("CC_COMP=%s %s" % (spack_cxx, cxx_flags))
                buildopts.append("FOPTS=-Kfast -Knotemparraystack %s" % " ".join(fflags))
        else:
            raise InstallError(
                "Spack does not yet have support for building "
                "BerkeleyGW with compiler %s" % spec.compiler
            )

        if "+hdf5" in spec:
            mathflags.append("-DHDF5")
            buildopts.append("HDF5INCLUDE=%s" % spec["hdf5"].prefix.include)
            buildopts.append("HDF5LIB=%s" % spec["hdf5:hl,fortran"].libs.ld_flags)

        if "+elpa" in spec:
            mathflags.append("-DUSEELPA")
            elpa = spec["elpa"]

            if "+openmp" in spec:
                elpa_suffix = "_openmp"
            else:
                elpa_suffix = ""

            elpa_incdir = elpa.headers.directories[0]
            elpa_libs = join_path(
                elpa.libs.directories[0], "libelpa%s.%s" % (elpa_suffix, dso_suffix)
            )

            buildopts.append("ELPALIB=%s" % elpa_libs)
            buildopts.append("ELPAINCLUDE=%s" % join_path(elpa_incdir, "modules"))

        buildopts.append("MATHFLAG=%s" % " ".join(mathflags))

        make("all-flavors", *buildopts)

    def install(self, spec, prefix):
        make("install", "INSTDIR=%s" % prefix)
