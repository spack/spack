# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from collections import defaultdict

from spack.package import *
from spack.util.environment import is_system_path


class Icon(AutotoolsPackage, CudaPackage):
    """Icosahedral Nonhydrostatic Weather and Climate Model."""

    homepage = "https://code.mpimet.mpg.de/projects/iconpublic"
    url = "https://gitlab.dkrz.de/icon/icon/-/archive/icon-2.6.6/icon-icon-2.6.6.tar.gz"
    git = "git@gitlab.dkrz.de:icon/icon.git"

    maintainers("dominichofer")

    version("develop", submodules=True)
    version("2.6.6", tag="icon-2.6.6", submodules=True)

    # The variants' default follow those of ICON as described in
    # https://gitlab.dkrz.de/icon/icon/-/blob/icon-2.6.6/configure#L1457-1563

    # Optional Features:
    variant("silent-rules", default=True, description="Less verbose build output")

    # Model Features:
    variant("atmo", default=True, description="Enable the atmosphere component")
    variant("edmf", default=True, description="Enable the EDMF turbulence component")
    variant("les", default=True, description="Enable the Large-Eddy Simulation component")
    variant("upatmo", default=True, description="Enable the upper atmosphere component")
    variant("ocean", default=True, description="Enable the ocean component")
    variant("jsbach", default=True, description="Enable the land component")
    variant("waves", default=False, description="Enable the surface wave component")
    variant("coupling", default=True, description="Enable the coupling")
    variant("aes", default=True, description="Enable the AES physics package")
    variant("ecrad", default=False, description="Enable usage of the ECMWF radiation scheme")
    variant(
        "rte-rrtmgp",
        default=True,
        description="Enable usage of the RTE+RRTMGP toolbox for radiation calculations",
    )
    variant(
        "rttov", default=False, description="Enable usage of the radiative transfer model for TOVS"
    )
    variant("dace", default=False, description="Enable the DACE modules for data assimilation")
    variant("emvorado", default=False, description="Enable the radar forward operator EMVORADO")
    variant(
        "art", default=False, description="Enable the aerosols and reactive trace component ART"
    )

    # Infrastructural Features:
    variant("mpi", default=True, description="Enable MPI (parallelization) support")
    variant(
        "active-target-sync",
        default=False,
        description="Enable MPI active target mode (otherwise, passive target mode is used)",
    )
    variant("openmp", default=False, description="Enable OpenMP support")
    variant("gpu", default=False, description="Enable GPU support")
    variant("realloc-buf", default=False, description="Enable reallocatable communication buffer")
    variant("grib2", default=False, description="Enable GRIB2 I/O")
    variant(
        "parallel-netcdf",
        default=False,
        description="Enable usage of the parallel features of NetCDF",
    )
    variant("cdi-pio", default=False, description="Enable usage of the parallel features of CDI")
    variant("sct", default=False, description="Enable the SCT timer")
    variant("yaxt", default=False, description="Enable the YAXT data exchange")

    claw_values = ("std", "validate")
    variant(
        "claw",
        default="none",
        values=("none",) + claw_values,
        description="Enable CLAW preprocessing",
    )

    serialization_values = ("read", "perturb", "create")
    variant(
        "serialization",
        default="none",
        values=("none",) + serialization_values,
        description="Enable the Serialbox2 serialization",
    )
    variant("testbed", default=False, description="Enable ICON Testbed infrastructure")

    # Optimization Features:
    variant("loop-exchange", default=True, description="Enable loop exchange")
    variant(
        "vectorized-lrtm",
        default=False,
        description="Enable the parallelization-invariant version of LRTM",
    )
    variant("mixed-precision", default=False, description="Enable mixed precision dycore")
    variant(
        "pgi-inlib",
        default=False,
        description="Enable PGI/NVIDIA cross-file function inlining via an inline library",
    )
    variant("nccl", default=False, description="Enable NCCL for communication")

    depends_on("libxml2", when="+coupling")
    depends_on("libxml2", when="+art")

    depends_on("rttov +hdf5", when="+rttov")
    depends_on("rttov ~openmp", when="+rttov ~openmp")

    for x in serialization_values:
        depends_on("serialbox +fortran ~shared", when="serialization={0}".format(x))

    depends_on("libcdi-pio +fortran +netcdf", when="+cdi-pio")
    depends_on("libcdi-pio grib2=eccodes", when="+cdi-pio +grib2")
    depends_on("libcdi-pio +mpi", when="+cdi-pio+mpi")

    depends_on("eccodes", when="+grib2 ~cdi-pio")
    depends_on("eccodes +fortran", when="+emvorado")

    depends_on("yaxt +fortran", when="+cdi-pio")
    depends_on("lapack")
    depends_on("blas")
    depends_on("netcdf-fortran")

    depends_on("netcdf-c", when="~cdi-pio")
    depends_on("netcdf-c", when="+coupling")
    depends_on("netcdf-c +mpi", when="+parallel-netcdf ~cdi-pio")

    depends_on("hdf5 +szip +hl +fortran", when="+emvorado")
    depends_on("hdf5 +szip", when="+sct")

    depends_on("zlib", when="+emvorado")
    depends_on("mpi", when="+mpi")

    depends_on("python", type="build")
    depends_on("perl", type="build")
    depends_on("cmake@3.18:", type="build")

    for x in claw_values:
        depends_on("claw", type="build", when="claw={0}".format(x))

    conflicts("claw=validate", when="serialization=none")

    for x in claw_values:
        conflicts("+sct", when="claw={0}".format(x))

    conflicts("+dace", when="~mpi")
    conflicts("+emvorado", when="~mpi")
    conflicts("+loop-exchange", when="+gpu")

    conflicts("~cuda", when="+gpu")
    conflicts("+cuda", when="~gpu")

    def configure_args(self):
        config_args = ["--disable-rpaths"]
        config_vars = defaultdict(list)
        libs = LibraryList([])

        for x in [
            "atmo",
            "edmf",
            "les",
            "upatmo",
            "ocean",
            "jsbach",
            "waves",
            "coupling",
            "aes",
            "ecrad",
            "rte-rrtmgp",
            "rttov",
            "dace",
            "emvorado",
            "art",
            "mpi",
            "active-target-sync",
            "openmp",
            "gpu",
            "realloc-buf",
            "grib2",
            "parallel-netcdf",
            "sct",
            "yaxt",
            "testbed",
            "loop-exchange",
            "vectorized-lrtm",
            "mixed-precision",
            "pgi-inlib",
            "nccl",
            "silent-rules",
        ]:
            config_args += self.enable_or_disable(x)

        if "+cdi-pio" in self.spec:
            config_args.extend(["--enable-cdi-pio", "--with-external-cdi", "--with-external-yaxt"])

        if self.compiler.name == "gcc":
            config_vars["CFLAGS"].append("-g")
            config_vars["ICON_CFLAGS"].append("-O3")
            config_vars["ICON_BUNDLED_CFLAGS"].append("-O2")
            config_vars["FCFLAGS"].extend(
                [
                    "-g",
                    "-fmodule-private",
                    "-fimplicit-none",
                    "-fmax-identifier-length=63",
                    "-Wall",
                    "-Wcharacter-truncation",
                    "-Wconversion",
                    "-Wunderflow",
                    "-Wunused-parameter",
                    "-Wno-surprising",
                    "-fall-intrinsics",
                ]
            )
            config_vars["ICON_FCFLAGS"].extend(
                [
                    "-O2",
                    "-fbacktrace",
                    "-fbounds-check",
                    "-fstack-protector-all",
                    "-finit-real=nan",
                    "-finit-integer=-2147483648",
                    "-finit-character=127",
                ]
            )
            config_vars["ICON_OCEAN_FCFLAGS"].append("-O3")

            # Version-specific workarounds:
            fc_version = self.compiler.version
            if fc_version >= ver(10):
                config_vars["ICON_FCFLAGS"].append("-fallow-argument-mismatch")
                config_vars["ICON_OCEAN_FCFLAGS"].append("-fallow-argument-mismatch")
                if "+ecrad" in self.spec:
                    # For externals/ecrad/ifsaux/random_numbers_mix.F90:
                    config_vars["ICON_ECRAD_FCFLAGS"].append("-fallow-invalid-boz")
        elif self.compiler.name == "intel":
            config_vars["CFLAGS"].extend(
                ["-g", "-gdwarf-4", "-O3", "-qno-opt-dynamic-align", "-ftz"]
            )
            config_vars["FCFLAGS"].extend(["-g", "-gdwarf-4", "-traceback", "-fp-model source"])
            config_vars["ICON_FCFLAGS"].extend(["-O2", "-assume realloc_lhs", "-ftz"])
            config_vars["ICON_OCEAN_FCFLAGS"].extend(
                [
                    "-O3",
                    "-assume norealloc_lhs",
                    "-reentrancy threaded",
                    "-qopt-report-file=stdout",
                    "-qopt-report=0",
                    "-qopt-report-phase=vec",
                ]
            )
            config_args.append("--enable-intel-consistency")
        elif self.compiler.name == "nag":
            config_vars["CFLAGS"].append("-g")
            config_vars["ICON_CFLAGS"].append("-O3")
            config_vars["ICON_BUNDLED_CFLAGS"].append("-O2")
            config_vars["FCFLAGS"].extend(
                ["-g", "-Wc,-g", "-O0", "-colour", "-f2008", "-w=uep", "-float-store", "-nan"]
            )
            if "~openmp" in self.spec:
                # The -openmp option is incompatible with the -gline option:
                config_vars["FCFLAGS"].append("-gline")
            config_vars["ICON_FCFLAGS"].extend(
                [
                    "-Wc,-pipe",
                    "-Wc,--param,max-vartrack-size=200000000",
                    "-Wc,-mno-fma",
                    # Spack compiler wrapper (see the respective compilers.yaml)
                    # injects '-mismatch', which is incompatible with '-C=calls'
                    # Therefore, we specify the following flags instead of a single
                    # '-C=all', which implies '-C=calls'.
                    "-C=alias",
                    "-C=array",
                    "-C=bits",
                    "-C=dangling",
                    "-C=do",
                    "-C=intovf",
                    "-C=present",
                    "-C=pointer",
                    "-C=recursion",
                ]
            )
            config_vars["ICON_BUNDLED_FCFLAGS"] = []
        elif self.compiler.name in ["pgi", "nvhpc"]:
            config_vars["CFLAGS"].extend(["-g", "-O2"])
            config_vars["FCFLAGS"].extend(
                ["-g", "-O", "-Mrecursive", "-Mallocatable=03", "-Mbackslash"]
            )

            if "+gpu" in self.spec:
                config_vars["FCFLAGS"].extend(
                    [
                        "-acc=verystrict",
                        "-Minfo=accel,inline",
                        "-gpu=cc{0}".format(self.spec.variants["cuda_arch"].value[0]),
                    ]
                )
        elif self.compiler.name == "cce":
            config_vars["CFLAGS"].append("-g")
            config_vars["ICON_CFLAGS"].append("-O3")
            if self.spec.satisfies("%cce@13.0.0+coupling"):
                # For externals/yac/tests/test_interpolation_method_conserv.c:
                config_vars["ICON_YAC_CFLAGS"].append("-O2")
            config_vars["FCFLAGS"].extend(
                [
                    "-hadd_paren",
                    "-r am",
                    "-Ktrap=divz,ovf,inv",
                    "-hflex_mp=intolerant",
                    "-hfp0",
                    "-O0",
                ]
            )
            if "+gpu" in self.spec:
                config_vars["FCFLAGS"].extend(["-hacc"])
        elif self.compiler.name == "aocc":
            config_vars["CFLAGS"].extend(["-g", "-O2"])
            config_vars["FCFLAGS"].extend(["-g", "-O2"])
            if self.spec.satisfies("~cdi-pio+yaxt"):
                # Enable the PGI/Cray (NO_2D_PARAM) workaround for the test
                # suite of the bundled YAXT (apply also when not self.run_tests
                # to make sure we get identical installations):
                config_vars["ICON_YAXT_FCFLAGS"].append("-DNO_2D_PARAM")
        else:
            config_vars["CFLAGS"].extend(["-g", "-O2"])
            config_vars["FCFLAGS"].extend(["-g", "-O2"])

        if "+coupling" in self.spec or "+art" in self.spec:
            xml2_spec = self.spec["libxml2"]
            libs += xml2_spec.libs
            # Account for the case when libxml2 is an external package installed
            # to a system directory, which means that Spack will not inject the
            # required -I flag with the compiler wrapper:
            if is_system_path(xml2_spec.prefix):
                xml2_headers = xml2_spec.headers
                # We, however, should filter the pure system directories out:
                xml2_headers.directories = [
                    d for d in xml2_headers.directories if not is_system_path(d)
                ]
                config_vars["CPPFLAGS"].append(xml2_headers.include_flags)

        serialization = self.spec.variants["serialization"].value
        if serialization == "none":
            config_args.append("--disable-serialization")
        else:
            config_args.extend(
                [
                    "--enable-serialization={0}".format(serialization),
                    "--enable-explicit-fpp",
                    "SB2PP={0}".format(self.spec["serialbox"].pp_ser),
                ]
            )
            libs += self.spec["serialbox:fortran"].libs
            # static libs from serialbox need libstdc++ to link
            config_vars["LIBS"].extend(["-lstdc++ -lstdc++fs"])

        if "+cdi-pio" in self.spec:
            libs += self.spec["libcdi-pio:fortran"].libs

        if "+emvorado" in self.spec:
            libs += self.spec["eccodes:fortran"].libs

        if "+grib2~cdi-pio" in self.spec:
            libs += self.spec["eccodes:c"].libs

        if "+cdi-pio" in self.spec:
            libs += self.spec["yaxt:fortran"].libs

        if "+rttov" in self.spec:
            libs += self.spec["rttov"].libs

        libs += self.spec["lapack:fortran"].libs
        libs += self.spec["blas:fortran"].libs
        libs += self.spec["netcdf-fortran"].libs

        if "+coupling" in self.spec or "~cdi-pio" in self.spec:
            libs += self.spec["netcdf-c"].libs

        if "+emvorado" in self.spec or "+rttov" in self.spec:
            libs += self.spec["hdf5:fortran,hl"].libs
        elif "+sct" in self.spec:
            libs += self.spec["hdf5"].libs

        if "+emvorado" in self.spec:
            libs += self.spec["zlib"].libs

        if "+mpi" in self.spec:
            config_args.extend(
                [
                    "CC=" + self.spec["mpi"].mpicc,
                    "FC=" + self.spec["mpi"].mpifc,
                    # We cannot provide a universal value for MPI_LAUNCH, therefore
                    # we have to disable the MPI checks:
                    "--disable-mpi-checks",
                ]
            )

        claw = self.spec.variants["claw"].value
        if claw == "none":
            config_args.append("--disable-claw")
        else:
            config_args.extend(
                [
                    "--enable-claw={0}".format(claw),
                    "CLAW={0}".format(self.spec["claw"].prefix.bin.clawfc),
                ]
            )
            config_vars["CLAWFLAGS"].append(self.spec["netcdf-fortran"].headers.include_flags)
            if "+cdi-pio" in self.spec:
                config_vars["CLAWFLAGS"].append(self.spec["libcdi-pio"].headers.include_flags)

        if "~gpu" in self.spec:
            config_args.append("--disable-gpu")
        else:
            config_args.extend(["NVCC={0}".format(self.spec["cuda"].prefix.bin.nvcc)])

            libs += self.spec["cuda"].libs

            cuda_host_compiler = self.compiler.cxx
            cuda_host_compiler_stdcxx_libs = self.compiler.stdcxx_libs

            config_vars["NVCFLAGS"].extend(
                [
                    "-g",
                    "-O3",
                    "-ccbin {0}".format(cuda_host_compiler),
                    "-arch=sm_{0}".format(self.spec.variants["cuda_arch"].value[0]),
                ]
            )
            # cuda_host_compiler_stdcxx_libs might contain compiler-specific
            # flags (i.e. not the linker -l<library> flags), therefore we put
            # the value to the config_flags directly.
            config_vars["LIBS"].extend(cuda_host_compiler_stdcxx_libs)

        # Finalize the LIBS variable (we always put the real collected
        # libraries to the front):
        config_vars["LIBS"].insert(0, libs.link_flags)

        # Help the libtool scripts of the bundled libraries find the correct
        # paths to the external libraries. Specify the library search (-L) flags
        # in the reversed order
        # (see https://gitlab.dkrz.de/icon/icon#icon-dependencies):
        # and for non-system directories only:
        config_vars["LDFLAGS"].extend(
            ["-L{0}".format(d) for d in reversed(libs.directories) if not is_system_path(d)]
        )

        config_args.extend(
            ["{0}={1}".format(var, " ".join(val)) for var, val in config_vars.items()]
        )

        return config_args

    @run_after("configure")
    def adjust_rttov_macro(self):
        if "+rttov" in self.spec:
            rttov_major_version = self.spec["rttov"].version.up_to(1)
            if rttov_major_version != ver(13):
                filter_file(
                    "_RTTOV_VERSION=13",
                    "_RTTOV_VERSION={0}".format(rttov_major_version),
                    "icon.mk",
                    string=True,
                    backup=False,
                )

    def build(self, spec, prefix):
        claw = self.spec.variants["claw"].value
        if claw != "none" and make_jobs > 8:
            # Limit CLAW preprocessing to 8 parallel jobs to avoid
            # claw_f_lib.sh: fork: retry: Resource temporarily unavailable
            # ...
            # Error: Could not create the Java Virtual Machine.
            # Error: A fatal exception has occurred. Program will exit.
            make.jobs = 8
            make("preprocess")
            make.jobs = make_jobs
        make(*self.build_targets)

    @property
    def archive_files(self):
        # Archive files that are normally archived for AutotoolsPackage:
        archive = list(super(Icon, self).archive_files)
        # Archive makefiles:
        archive.extend([join_path(self.build_directory, f) for f in ["Makefile", "*.mk"]])
        return archive
