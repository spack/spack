# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty

from spack.package import *


class Hpctoolkit(AutotoolsPackage):
    """HPCToolkit is an integrated suite of tools for measurement and analysis
    of program performance on computers ranging from multicore desktop systems
    to the nation's largest supercomputers. By using statistical sampling of
    timers and hardware performance counters, HPCToolkit collects accurate
    measurements of a program's work, resource consumption, and inefficiency
    and attributes them to the full calling context in which they occur."""

    homepage = "http://hpctoolkit.org"
    git = "https://gitlab.com/hpctoolkit/hpctoolkit.git"
    maintainers("mwkrentel")

    tags = ["e4s"]

    test_requires_compiler = True

    version("develop", branch="develop")
    version("2023.03.stable", branch="release/2023.03")
    version("2023.03.01", commit="9e0daf2ad169f6c7f6c60408475b3c2f71baebbf")
    version("2022.10.01", commit="e8a5cc87e8f5ddfd14338459a4106f8e0d162c83")
    version("2022.05.15", commit="8ac72d9963c4ed7b7f56acb65feb02fbce353479")
    version("2022.04.15", commit="a92fdad29fc180cc522a9087bba9554a829ee002")
    version("2022.01.15", commit="0238e9a052a696707e4e65b2269f342baad728ae")
    version("2021.10.15", commit="a8f289e4dc87ff98e05cfc105978c09eb2f5ea16")
    version("2021.05.15", commit="004ea0c2aea6a261e7d5d216c24f8a703fc6c408")
    version("2021.03.01", commit="68a051044c952f0f4dac459d9941875c700039e7", deprecated=True)
    version("2020.08.03", commit="d9d13c705d81e5de38e624254cf0875cce6add9a", deprecated=True)
    version("2020.07.21", commit="4e56c780cffc53875aca67d6472a2fb3678970eb", deprecated=True)
    version("2020.06.12", commit="ac6ae1156e77d35596fea743ed8ae768f7222f19", deprecated=True)
    version("2020.03.01", commit="94ede4e6fa1e05e6f080be8dc388240ea027f769", deprecated=True)
    version("2019.12.28", commit="b4e1877ff96069fd8ed0fdf0e36283a5b4b62240", deprecated=True)
    version("2019.08.14", commit="6ea44ed3f93ede2d0a48937f288a2d41188a277c", deprecated=True)
    version("2018.12.28", commit="8dbf0d543171ffa9885344f32f23cc6f7f6e39bc", deprecated=True)
    version("2018.11.05", commit="d0c43e39020e67095b1f1d8bb89b75f22b12aee9", deprecated=True)

    # Options for MPI and hpcprof-mpi.  We always support profiling
    # MPI applications.  These options add hpcprof-mpi, the MPI
    # version of hpcprof.  Cray is a separate option for old systems
    # where an external MPI module doesn't work.
    variant(
        "cray",
        default=False,
        description="Build hpcprof-mpi for Cray systems (may require --dirty).",
    )

    variant(
        "cray-static",
        default=False,
        description="Build old rev of hpcprof-mpi statically on Cray systems.",
        when="@:2022.09+cray",
    )

    variant(
        "mpi",
        default=False,
        description="Build hpcprof-mpi, the MPI version of hpcprof "
        "(not available for 2022.10.01).",
    )

    # We can't build with both PAPI and perfmon for risk of segfault
    # from mismatched header files (unless PAPI installs the perfmon
    # headers).
    variant(
        "papi",
        default=True,
        description="Use PAPI instead of perfmon for access to "
        "the hardware performance counters.",
    )

    # Accelerator variants: cuda, rocm, etc.
    variant("cuda", default=False, description="Support CUDA on NVIDIA GPUs.", when="@2020.03:")

    variant(
        "level_zero",
        default=False,
        description="Support Level Zero on Intel GPUs.",
        when="@2022.04:",
    )

    variant(
        "gtpin",
        default=False,
        description="Support instrumenting Intel GPU kernels with Intel GT-Pin",
        when="@2022.05: +level_zero",
    )

    variant("opencl", default=False, description="Support offloading with OpenCL.")
    variant("rocm", default=False, description="Support ROCM on AMD GPUs.", when="@2022.04:")

    # Other variants.
    variant("debug", default=False, description="Build in debug (develop) mode.")
    variant("viewer", default=True, description="Include hpcviewer.")

    variant(
        "python", default=False, description="Support unwinding Python source.", when="@2023.03:"
    )

    boost_libs = (
        "+atomic +chrono +date_time +filesystem +system +thread +timer"
        " +graph +regex +shared +multithreaded visibility=global"
    )

    depends_on("binutils +libiberty", type="link", when="@2021:2022.06")
    depends_on("binutils +libiberty~nls", type="link", when="@2020.04:2020")
    depends_on("binutils@:2.33.1 +libiberty~nls", type="link", when="@:2020.03")
    depends_on("boost" + boost_libs)
    depends_on("bzip2+shared", type="link")
    depends_on("dyninst@12.1.0:", when="@2022.0:")
    depends_on("dyninst@10.2.0:", when="@2021.0:2021.12")
    depends_on("dyninst@9.3.2:", when="@:2020")
    depends_on("elfutils~nls", type="link")
    depends_on("gotcha@1.0.3:", when="@:2020.09")
    depends_on("intel-tbb+shared")
    depends_on("libdwarf", when="@:2022.06")
    depends_on("libiberty+pic", when="@2022.10:")
    depends_on("libmonitor+hpctoolkit~dlopen", when="@2021.00:")
    depends_on("libmonitor+hpctoolkit+dlopen", when="@:2020")
    depends_on("libmonitor@2023.02.13:", when="@2023.01:")
    depends_on("libmonitor@2021.11.08:", when="@2022.01:")
    depends_on("libunwind@1.4: +xz+pic")
    depends_on("mbedtls+pic", when="@:2022.03")
    depends_on("xerces-c transcoder=iconv")
    depends_on("xz+pic libs=static", type="link")
    depends_on("yaml-cpp@0.7.0: +shared", when="@2022.10:")
    depends_on("zlib+shared")

    depends_on("cuda", when="+cuda")
    depends_on("oneapi-level-zero", when="+level_zero")
    depends_on("oneapi-igc", when="+gtpin")
    depends_on("intel-gtpin", when="+gtpin")
    depends_on("opencl-c-headers", when="+opencl")

    depends_on("intel-xed+pic", when="target=x86_64:")
    depends_on("memkind", type=("build", "run"), when="@2021.05.01:")
    depends_on("papi", when="+papi")
    depends_on("libpfm4", when="~papi")
    depends_on("mpi", when="+cray")
    depends_on("mpi", when="+mpi")
    depends_on("hpcviewer@2022.10:", type="run", when="@2022.10: +viewer")
    depends_on("hpcviewer", type="run", when="+viewer")
    depends_on("python@3.10:", type=("build", "run"), when="+python")

    # Avoid 'link' dep, we don't actually link, and that adds rpath
    # that conflicts with app.
    depends_on("hip@4.5:", type=("build", "run"), when="+rocm")
    depends_on("hsa-rocr-dev@4.5:", type=("build", "run"), when="+rocm")
    depends_on("roctracer-dev@4.5:", type=("build", "run"), when="+rocm")
    depends_on("rocprofiler-dev@4.5:", type=("build", "run"), when="+rocm")

    conflicts("%gcc@:7", when="@2022.10:", msg="hpctoolkit requires gnu gcc 8.x or later")
    conflicts("%gcc@:6", when="@2021.00:2022.06", msg="hpctoolkit requires gnu gcc 7.x or later")
    conflicts("%gcc@:4", when="@:2020", msg="hpctoolkit requires gnu gcc 5.x or later")

    conflicts("^binutils@2.35:2.35.1", msg="avoid binutils 2.35 and 2.35.1 (spews errors)")
    conflicts("xz@5.2.7:5.2.8", msg="avoid xz 5.2.7:5.2.8 (broken symbol versions)")

    conflicts("+cray", when="@2022.10.01", msg="hpcprof-mpi is not available in 2022.10.01")
    conflicts("+mpi", when="@2022.10.01", msg="hpcprof-mpi is not available in 2022.10.01")

    conflicts(
        "^hip@5.3:", when="@:2022.12", msg="rocm 5.3 requires hpctoolkit 2023.03.01 or later"
    )

    # Fix the build for old revs with gcc 10.x and 11.x.
    patch("gcc10-enum.patch", when="@2020.01.01:2020.08 %gcc@10.0:")
    patch("511afd95b01d743edc5940c84e0079f462b2c23e.patch", when="@2019.08.01:2021.03 %gcc@11.0:")

    # Change python to python3 for some old revs that use a script
    # with /usr/bin/env python.
    depends_on("python@3.4:", type="build", when="@2020.03:2020.08")
    patch("python3.patch", when="@2020.03:2020.08")

    # Fix a bug where make would mistakenly overwrite hpcrun-fmt.h.
    # https://gitlab.com/hpctoolkit/hpctoolkit/-/merge_requests/751
    def patch(self):
        with working_dir(join_path("src", "lib", "prof-lean")):
            if os.access("hpcrun-fmt.txt", os.F_OK):
                os.rename("hpcrun-fmt.txt", "hpcrun-fmt.readme")

    flag_handler = AutotoolsPackage.build_system_flags

    def configure_args(self):
        spec = self.spec

        args = [
            "--with-boost=%s" % spec["boost"].prefix,
            "--with-bzip=%s" % spec["bzip2"].prefix,
            "--with-dyninst=%s" % spec["dyninst"].prefix,
            "--with-elfutils=%s" % spec["elfutils"].prefix,
            "--with-tbb=%s" % spec["intel-tbb"].prefix,
            "--with-libmonitor=%s" % spec["libmonitor"].prefix,
            "--with-libunwind=%s" % spec["libunwind"].prefix,
            "--with-xerces=%s" % spec["xerces-c"].prefix,
            "--with-lzma=%s" % spec["xz"].prefix,
            "--with-zlib=%s" % spec["zlib"].prefix,
        ]

        if spec.satisfies("@2022.10:"):
            args.append("--with-libiberty=%s" % spec["libiberty"].prefix)
        else:
            args.append("--with-binutils=%s" % spec["binutils"].prefix)
            args.append("--with-libdwarf=%s" % spec["libdwarf"].prefix)

        if spec.satisfies("@:2020.09"):
            args.append("--with-gotcha=%s" % spec["gotcha"].prefix)

        if spec.target.family == "x86_64":
            args.append("--with-xed=%s" % spec["intel-xed"].prefix)

        if spec.satisfies("@:2022.03"):
            args.append("--with-mbedtls=%s" % spec["mbedtls"].prefix)

        if spec.satisfies("@2021.05.01:"):
            args.append("--with-memkind=%s" % spec["memkind"].prefix)

        if spec.satisfies("+papi"):
            args.append("--with-papi=%s" % spec["papi"].prefix)
        else:
            args.append("--with-perfmon=%s" % spec["libpfm4"].prefix)

        if spec.satisfies("@2022.10:"):
            args.append("--with-yaml-cpp=%s" % spec["yaml-cpp"].prefix)

        if "+cuda" in spec:
            args.append("--with-cuda=%s" % spec["cuda"].prefix)

        if "+level_zero" in spec:
            args.append("--with-level0=%s" % spec["oneapi-level-zero"].prefix)

            # gtpin requires level_zero
            if "+gtpin" in spec:
                args.append("--with-gtpin=%s" % spec["intel-gtpin"].prefix)
                args.append("--with-igc=%s" % spec["oneapi-igc"].prefix)

        if "+opencl" in spec:
            args.append("--with-opencl=%s" % spec["opencl-c-headers"].prefix)

        if spec.satisfies("+rocm"):
            args.extend(
                [
                    "--with-rocm-hip=%s" % spec["hip"].prefix,
                    "--with-rocm-hsa=%s" % spec["hsa-rocr-dev"].prefix,
                    "--with-rocm-tracer=%s" % spec["roctracer-dev"].prefix,
                    "--with-rocm-profiler=%s" % spec["rocprofiler-dev"].prefix,
                ]
            )

        if spec.satisfies("+python"):
            p3config = join_path(spec["python"].prefix, "bin", "python3-config")
            args.append("--with-python=%s" % p3config)

        # MPI options for hpcprof-mpi. +cray supersedes +mpi.
        if spec.satisfies("+cray"):
            args.append("--enable-mpi-search=cray")
            if spec.satisfies("@:2022.09 +cray-static"):
                args.append("--enable-all-static")
            else:
                args.append("HPCPROFMPI_LT_LDFLAGS=-dynamic")

        elif spec.satisfies("+mpi"):
            args.append("MPICXX=%s" % spec["mpi"].mpicxx)

        # Make sure MPICXX is not picked up through the environment.
        else:
            args.append("MPICXX=")

        if spec.satisfies("+debug"):
            args.append("--enable-develop")

        return args

    # We only want hpctoolkit and hpcviewer paths and man paths in the
    # module file.  The run dependencies are all curried into hpctoolkit
    # and we don't want to risk exposing a package if the application
    # uses a different version of the same package.
    def setup_run_environment(self, env):
        spec = self.spec
        env.clear()
        env.prepend_path("PATH", spec.prefix.bin)
        env.prepend_path("MANPATH", spec.prefix.share.man)
        env.prepend_path("CPATH", spec.prefix.include)
        env.prepend_path("LD_LIBRARY_PATH", spec.prefix.lib.hpctoolkit)
        if "+viewer" in spec:
            env.prepend_path("PATH", spec["hpcviewer"].prefix.bin)
            env.prepend_path("MANPATH", spec["hpcviewer"].prefix.share.man)

    # Build tests (spack install --run-tests).  Disable the default
    # spack tests and run autotools 'make check', but only from the
    # tests directory.
    build_time_test_callbacks = []  # type: List[str]
    install_time_test_callbacks = []  # type: List[str]

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        if not self.spec.satisfies("@2022:"):
            tty.warn("requires 2022.01.15 or later")
            return

        with working_dir("tests"):
            make("check")

    # Post-Install tests (spack test run).  These are the same tests
    # but with a different Makefile that works outside the build
    # directory.
    @run_after("install")
    def copy_test_files(self):
        if self.spec.satisfies("@2022:"):
            self.cache_extra_test_sources(["tests"])

    def test_run_sort(self):
        """build and run selection sort unit test"""
        if not self.spec.satisfies("@2022:"):
            raise SkipTest("No tests exist for versions prior to 2022.01.15")

        test_dir = self.test_suite.current_test_cache_dir.tests
        with working_dir(test_dir):
            make = which("make")
            make("-f", "Makefile.spack", "all")

            run_sort = which(join_path(".", "run-sort"))
            assert run_sort, "run-sort is missing"

            run_sort()
