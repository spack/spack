# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Vasp(MakefilePackage):
    """
    The Vienna Ab initio Simulation Package (VASP)
    is a computer program for atomic scale materials modelling,
    e.g. electronic structure calculations
    and quantum-mechanical molecular dynamics, from first principles.
    """

    homepage = "https://vasp.at"
    url = "file://{0}/vasp.5.4.4.pl2.tgz".format(os.getcwd())
    manual_download = True

    version("6.3.2", sha256="f7595221b0f9236a324ea8afe170637a578cdd5a837cc7679e7f7812f6edf25a")
    version("6.3.0", sha256="adcf83bdfd98061016baae31616b54329563aa2739573f069dd9df19c2071ad3")
    version("6.2.0", sha256="49e7ba351bd634bc5f5f67a8ef1e38e64e772857a1c02f602828898a84197e25")
    version("6.1.1", sha256="e37a4dfad09d3ad0410833bcd55af6b599179a085299026992c2d8e319bf6927")
    version("5.4.4.pl2", sha256="98f75fd75399a23d76d060a6155f4416b340a1704f256a00146f89024035bc8e")
    version("5.4.4", sha256="5bd2449462386f01e575f9adf629c08cb03a13142806ffb6a71309ca4431cfb3")

    resource(
        name="vaspsol",
        git="https://github.com/henniggroup/VASPsol.git",
        tag="V1.0",
        when="+vaspsol",
    )

    variant("openmp", default=False, description="Enable openmp build")
    with when("+openmp"):
        conflicts("^fftw~openmp")
        conflicts("^amdfftw~openmp")
        conflicts("^amdblis threads=none")
        conflicts("^amdblis threads=pthreads")
        conflicts("^openblas threads=none")
        conflicts("^openblas threads=pthreads")

    variant("scalapack", default=False, description="Enables build with SCALAPACK")

    variant("cuda", default=False, description="Enables running on Nvidia GPUs")
    variant("fftlib", default=False, description="Enables fftlib build")
    with when("+fftlib"):
        conflicts("@:6.1.1", msg="fftlib support started from 6.2.0")
        conflicts("~openmp", msg="fftlib is intended to be used with openmp")

    variant(
        "vaspsol",
        default=False,
        description="Enable VASPsol implicit solvation model\n"
        "https://github.com/henniggroup/VASPsol",
    )
    variant("shmem", default=True, description="Enable use_shmem build flag")

    depends_on("rsync", type="build")
    depends_on("blas")
    depends_on("lapack")
    depends_on("fftw-api")
    depends_on("mpi", type=("build", "link", "run"))
    depends_on("scalapack", when="+scalapack")
    depends_on("cuda", when="+cuda")
    depends_on("qd", when="%nvhpc")

    conflicts(
        "%gcc@:8", msg="GFortran before 9.x does not support all features needed to build VASP"
    )
    conflicts("+vaspsol", when="+cuda", msg="+vaspsol only available for CPU")
    conflicts("+openmp", when="@:6.1.1", msg="openmp support started from 6.2")

    parallel = False

    def edit(self, spec, prefix):
        if "%gcc" in spec:
            if "+openmp" in spec:
                make_include = join_path("arch", "makefile.include.linux_gnu_omp")
            else:
                make_include = join_path("arch", "makefile.include.linux_gnu")
        elif "%nvhpc" in spec:
            make_include = join_path("arch", "makefile.include.linux_pgi")
            filter_file("-pgc++libs", "-c++libs", make_include, string=True)
            filter_file("pgcc", spack_cc, make_include)
            filter_file("pgc++", spack_cxx, make_include, string=True)
            filter_file("pgfortran", spack_fc, make_include)
            filter_file(
                "/opt/pgi/qd-2.3.17/install/include", spec["qd"].prefix.include, make_include
            )
            filter_file("/opt/pgi/qd-2.3.17/install/lib", spec["qd"].prefix.lib, make_include)
        elif "%aocc" in spec:
            if "+openmp" in spec:
                if "@6.3.0" in spec:
                    copy(
                        join_path("arch", "makefile.include.gnu_ompi_aocl_omp"),
                        join_path("arch", "makefile.include.linux_aocc_omp"),
                    )
                    make_include = join_path("arch", "makefile.include.linux_aocc_omp")

                elif "@6.3.2:" in spec:
                    make_include = join_path("arch", "makefile.include.aocc_ompi_aocl_omp")
                else:
                    copy(
                        join_path("arch", "makefile.include.linux_gnu_omp"),
                        join_path("arch", "makefile.include.linux_aocc_omp"),
                    )
                    make_include = join_path("arch", "makefile.include.linux_aocc_omp")
            else:
                if "@6.3.0:" in spec:
                    copy(
                        join_path("arch", "makefile.include.gnu_ompi_aocl"),
                        join_path("arch", "makefile.include.linux_aocc"),
                    )
                    make_include = join_path("arch", "makefile.include.linux_aocc")
                if "@6.3.2:" in spec:
                    make_include = join_path("arch", "makefile.include.aocc_ompi_aocl")
                else:
                    copy(
                        join_path("arch", "makefile.include.linux_gnu"),
                        join_path("arch", "makefile.include.linux_aocc"),
                    )
                    make_include = join_path("arch", "makefile.include.linux_aocc_omp")
            filter_file("^CC_LIB[ ]{0,}=.*$", "CC_LIB={0}".format(spack_cc), make_include)
            if "@6.3.0:" in spec:
                filter_file("gcc", "{0} {1}".format(spack_fc, "-Mfree"), make_include, string=True)
            else:
                filter_file("gcc", "{0}".format(spack_fc), make_include, string=True)
                filter_file("g++", spack_cxx, make_include, string=True)

            filter_file("^CFLAGS_LIB[ ]{0,}=.*$", "CFLAGS_LIB = -O3", make_include)
            filter_file("^FFLAGS_LIB[ ]{0,}=.*$", "FFLAGS_LIB = -O3", make_include)
            filter_file("^OFLAG[ ]{0,}=.*$", "OFLAG = -O3", make_include)
            filter_file(
                "^FC[ ]{0,}=.*$", "FC = {0}".format(spec["mpi"].mpifc), make_include, string=True
            )
            filter_file(
                "^FCL[ ]{0,}=.*$",
                '"FCL = {0}".format(spec["mpi"].mpifc)',
                make_include,
                string=True,
            )
            filter_file(
                "-fallow-argument-mismatch", " -fno-fortran-main", make_include, string=True
            )

            filter_file("^OBJECTS_LIB[ ]{0,}=.*$", "OBJECTS_LIB ?=", make_include)
            filter_file("-march=native", " ", make_include)
        else:
            if "+openmp" in spec:
                make_include = join_path(
                    "arch", "makefile.include.linux_{0}_omp".format(spec.compiler.name)
                )
            else:
                make_include = join_path("arch", "makefile.include.linux_" + spec.compiler.name)

        # Recent versions of vasp have renamed the makefile.include files
        # to leave out the linux_ string
        if not os.path.exists(make_include):
            make_include = make_include.replace("linux_", "")
        os.rename(make_include, "makefile.include")

        # This bunch of 'filter_file()' is to make these options settable
        # as environment variables
        filter_file("^CPP_OPTIONS[ ]{0,}=[ ]{0,}", "CPP_OPTIONS ?= ", "makefile.include")
        filter_file("^FFLAGS[ ]{0,}=[ ]{0,}", "FFLAGS ?= ", "makefile.include")

        filter_file("^LIBDIR[ ]{0,}=.*$", "", "makefile.include")
        filter_file("^BLAS[ ]{0,}=.*$", "BLAS ?=", "makefile.include")
        filter_file("^LAPACK[ ]{0,}=.*$", "LAPACK ?=", "makefile.include")
        filter_file("^FFTW[ ]{0,}?=.*$", "FFTW ?=", "makefile.include")
        filter_file("^MPI_INC[ ]{0,}=.*$", "MPI_INC ?=", "makefile.include")
        filter_file("-DscaLAPACK.*$\n", "", "makefile.include")
        filter_file("^SCALAPACK[ ]{0,} =.*$", "SCALAPACK ?=", "makefile.include")

        if "+cuda" in spec:
            filter_file("^OBJECTS_GPU[ ]{0,}=.*$", "OBJECTS_GPU ?=", "makefile.include")

            filter_file("^CPP_GPU[ ]{0,}=.*$", "CPP_GPU ?=", "makefile.include")

            filter_file("^CFLAGS[ ]{0,}=.*$", "CFLAGS ?=", "makefile.include")

        if "+fftlib" in spec:
            filter_file("^#FCL[ ]{0,}=fftlib.o", "FCL += fftlib/fftlib.o", "makefile.include")
            filter_file("^#CXX_FFTLIB", "CXX_FFTLIB", "makefile.include")
            filter_file("^#INCS_FFTLIB", "INCS_FFTLIB", "makefile.include")
            filter_file("^#LIBS", "LIBS", "makefile.include")
            filter_file(
                "LIBS[ ]{0,}=.*$", "LIBS=-lstdc++ fftlib/fftlib.o -ldl", "makefile.include"
            )
        if "+vaspsol" in spec:
            copy("VASPsol/src/solvation.F", "src/")

    def setup_build_environment(self, spack_env):
        spec = self.spec

        cpp_options = [
            "-DMPI -DMPI_BLOCK=8000",
            "-Duse_collective",
            "-DCACHE_SIZE=4000",
            "-Davoidalloc",
            "-Duse_bse_te",
            "-Dtbdyn",
        ]

        if "+shmem" in spec:
            cpp_options.append("-Duse_shmem")

        if "%nvhpc" in self.spec:
            cpp_options.extend(['-DHOST=\\"LinuxPGI\\"', "-DPGI16", "-Dqd_emulate"])
        elif "%aocc" in self.spec:
            cpp_options.extend(
                [
                    '-DHOST=\\"LinuxAMD\\"',
                    "-Dfock_dblbuf",
                    "-Dsysv",
                    "-Dshmem_bcast_buffer",
                    "-DNGZhalf",
                ]
            )
            if "@6.3.0:" and "^amdfftw@4.0:" in self.spec:
                cpp_options.extend(["-Dfftw_cache_plans", "-Duse_fftw_plan_effort"])
            if "+openmp" in self.spec:
                cpp_options.extend(["-D_OPENMP"])
            cpp_options.extend(["-Mfree "])
        else:
            cpp_options.append('-DHOST=\\"LinuxGNU\\"')

        if self.spec.satisfies("@6:"):
            cpp_options.append("-Dvasp6")

        cflags = ["-fPIC", "-DADD_"]
        fflags = []
        if "%gcc" in spec or "%intel" in spec:
            fflags.append("-w")
        elif "%nvhpc" in spec:
            fflags.extend(["-Mnoupcase", "-Mbackslash", "-Mlarge_arrays"])
        elif "%aocc" in spec:
            fflags.extend(["-fno-fortran-main", "-Mbackslash"])
            objects_lib = ["linpack_double.o", "getshmem.o"]
            spack_env.set("OBJECTS_LIB", " ".join(objects_lib))

        spack_env.set("BLAS", spec["blas"].libs.ld_flags)
        spack_env.set("LAPACK", spec["lapack"].libs.ld_flags)
        if "^amdfftw" in spec:
            spack_env.set("AMDFFTW_ROOT", spec["fftw-api"].prefix)
        else:
            spack_env.set("FFTW", spec["fftw-api"].libs.ld_flags)
        spack_env.set("MPI_INC", spec["mpi"].prefix.include)

        if "%nvhpc" in spec:
            spack_env.set("QD", spec["qd"].prefix)

        if "+scalapack" in spec:
            cpp_options.append("-DscaLAPACK")
            spack_env.set("SCALAPACK", spec["scalapack"].libs.ld_flags)

        if "+cuda" in spec:
            cpp_gpu = [
                "-DCUDA_GPU",
                "-DRPROMU_CPROJ_OVERLAP",
                "-DCUFFT_MIN=28",
                "-DUSE_PINNED_MEMORY",
            ]

            objects_gpu = [
                "fftmpiw.o",
                "fftmpi_map.o",
                "fft3dlib.o",
                "fftw3d_gpu.o",
                "fftmpiw_gpu.o",
            ]

            cflags.extend(["-DGPUSHMEM=300", "-DHAVE_CUBLAS"])

            spack_env.set("CUDA_ROOT", spec["cuda"].prefix)
            spack_env.set("CPP_GPU", " ".join(cpp_gpu))
            spack_env.set("OBJECTS_GPU", " ".join(objects_gpu))

        if "+vaspsol" in spec:
            cpp_options.append("-Dsol_compat")

        if spec.satisfies("%gcc@10:"):
            fflags.append("-fallow-argument-mismatch")
        if spec.satisfies("%aocc"):
            fflags.append("-fno-fortran-main -Mbackslash -ffunc-args-alias")

        # Finally
        spack_env.set("CPP_OPTIONS", " ".join(cpp_options))
        spack_env.set("CFLAGS", " ".join(cflags))
        spack_env.set("FFLAGS", " ".join(fflags))

    def build(self, spec, prefix):
        if "+cuda" in self.spec:
            make("gpu", "gpu_ncl")
        else:
            make("std", "gam", "ncl")

    def install(self, spec, prefix):
        install_tree("bin/", prefix.bin)
