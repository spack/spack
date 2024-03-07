# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import subprocess

from spack.package import *
from spack.util.environment import path_put_first, set_env


class Chapel(AutotoolsPackage, CudaPackage, ROCmPackage):
    """Chapel is a modern programming language that is parallel, productive,
    portable, scalable and open-source."""

    homepage = "https://chapel-lang.org/"

    url = "https://github.com/chapel-lang/chapel/archive/refs/tags/1.33.0.tar.gz"
    git = "https://github.com/chapel-lang/chapel.git"

    test_requires_compiler = True

    executables = ["^chpl$", "^chpldoc$"]

    # A list of GitHub accounts to notify when the package is updated.
    maintainers("arezaii")

    # See https://spdx.org/licenses/ for a list.
    license("Apache-2.0")

    version("1.34.0", branch="main")

    version("1.33.0", sha256="c7dfe691a043b6a5dcbea6fe7607ca030014f1a8019744c4c99f67caa8829ba3")
    version("1.32.0", sha256="a359032b4355774e250fb2796887b3bbf58d010c468faba97f7b471bc6bab57d")
    version("1.31.0", sha256="bf9a63f7e5d1f247e8680c9a07aeb330cbbf199777a282408100a87dda95918f")
    version("1.30.0", sha256="d7d82f64f405b8c03e2ce6353d16aba5a261d3f0c63dc3bb64ea3841cfa597b9")

    compilers = (
        "allinea",
        "clang",
        "cray-prgenv-allinea",
        "cray-prgenv-cray",
        "cray-prgenv-gnu",
        "cray-prgenv-intel",
        "cray-prgenv-pgi",
        "gnu",
        "ibm",
        "intel",
        "llvm",
        "pgi",
        "unset",
    )

    launcher_names = (
        "amudprun",
        "aprun",
        "gasnetrun_ibv",
        "gasnetrun_mpi",
        "mpirun4ofi",
        "lsf-gasnetrun_ibv",
        "pals",
        "pbs-aprun",
        "pbs-gasnetrun_ibv",
        "slurm-gasnetrun_ibv",
        "slurm-gasnetrun_mpi",
        "slurm-gasnetrun_ofi",
        "slurm-srun",
        "smp",
        "none",
        "unset",
    )

    # TODO: revise this list of mappings, probably need more logic for cce, see upc++
    compiler_map = {
        "aocc": "clang",
        "apple-clang": "clang",
        "arm": "clang",
        "clang": "clang",
        "cce": "cray-prgenv-cray",
        "cray-prgenv-cray": "cray",
        "cray-prgenv-gnu": "gnu",
        "cray-prgenv-intel": "intel",
        "cray-prgenv-pgi": "pgi",
        "dpcpp": "intel",
        "gcc": "gnu",
        "intel": "intel",
        "oneapi": "intel",
        "pgi": "pgi",
        "rocmcc": "clang",
        "unset": "unset",
    }

    # TODO: add other package dependencies
    package_module_dict = {
        "curl": "curl",
        "hdf5": "hdf5+hl~mpi",
        "libevent": "libevent",
        "protobuf": "py-protobuf",
        "ssl": "openssl",
        "yaml": "libyaml@0.1",
        "zmq": "libzmq",
    }

    platform_opts = (
        "cray-cs",
        "cray-xc",
        "cygwin32",
        "cygwin64",
        "darwin",
        "hpe-apollo",
        "hpe-cray-ex",
        "linux32",
        "linux64",
        "netbsd32",
        "netbsd64",
        "pwr6",
        "unset",
    )

    variant(
        "atomics",
        values=("unset", "cstdlib", "intrinsics", "locks"),
        default="unset",
        description="Select atomics implementation",
        multi=False,
    )

    variant("check", default=False, description="Run make check after installing the package")

    variant(
        "chpldoc", when="@1.34:", default=False, description="Build chpldoc in addition to chpl"
    )
    variant(
        "chpldoc", when="@main", default=False, description="Build chpldoc in addition to chpl"
    )

    variant(
        "comm",
        default="none",
        description="Build Chapel with multi-locale support",
        values=("gasnet", "none", "ofi"),
    )

    variant(
        "comm_substrate",
        default="unset",
        description="Build Chapel with mulit-locale support using the "
        "supplied CHPL_COMM_SUBSTRATE",
        values=("ibv", "ofi", "udp", "unset"),
        multi=False,
    )

    variant(
        "developer",
        values=(True, False),
        default=False,
        description="Build with developer flag to enable assertions and other checks",
    )

    variant(
        "gasnet_segment",
        default="unset",
        description="Build Chapel with multi-locale support using the "
        "supplied CHPL_GASNET_SEGMENT",
        values=("everything", "fast", "large", "unset"),
        multi=False,
    )

    variant(
        "gmp",
        description="Build with gmp support",
        default="spack",
        values=("bundled", "none", "spack", "system"),
        multi=False,
    )

    variant(
        "gpu_mem_strategy",
        description="The memory allocation strategy for GPU data",
        values=("array_on_device", "unified_memory"),
        default="array_on_device",
        multi=False,
    )

    variant(
        "host_arch",
        description="Host architecture of the build machine",
        values=("x86_64", "aarch64", "arm64", "unset"),
        default="unset",
        multi=False,
    )

    variant(
        "host_compiler",
        values=compilers,
        description="Compiler suite for building the Chapel compiler on CHPL_HOST_PLATFORM",
        default="unset",
    )

    variant(
        "host_jemalloc",
        values=("bundled", "none", "system", "unset"),
        default="unset",
        multi=False,
        description="Selects between no jemalloc, bundled jemalloc, or system jemalloc",
    )

    variant(
        "host_mem",
        values=("cstdlib", "jemalloc"),
        default="jemalloc",
        description="Memory management layer for the chpl compiler",
        multi=False,
    )

    variant(
        "host_platform",
        description="Host platform",
        default="unset",
        values=platform_opts,
        multi=False,
    )

    variant(
        "hwloc",
        description="Build with hwloc support",
        default="bundled",
        values=("bundled", "none"),
        multi=False,
    )

    variant(
        "launcher",
        values=launcher_names,
        default="unset",
        description="Launcher to use for running Chapel programs",
        multi=False,
    )

    variant(
        "lib_pic",
        values=("none", "pic"),
        default="none",
        description="Build position-independent code suitable for shared libraries",
    )

    variant(
        "libfabric",
        default="unset",
        description="When building with ofi support, specify libfabric option",
        values=("bundled", "system", "unset"),
        multi=False,
    )

    variant(
        "llvm",
        default="spack",
        description="LLVM backend type. Use value 'spack' to have spack "
        "handle the LLVM package",
        values=("bundled", "none", "spack", "system"),
    )

    variant(
        "module_tests",
        default=False,
        description="Run self-tests on selected modules after installing the package "
        "(may add several minutes to install time)",
    )

    variant(
        "package_modules",
        description="Include package module dependencies with spack",
        values=disjoint_sets(("none",), ("all",), package_module_dict.keys())
        .with_error("'none' or 'all' cannot be activated along with other package_modules")
        .with_default("none")
        .with_non_feature_values("none", "all"),
    )

    variant(
        "re2",
        description="Build with re2 support",
        default="bundled",
        values=("bundled", "none"),
        multi=False,
    )

    variant(
        "target_arch",
        description="Target architecture for cross compilation",
        default="unset",
        values=("x86_64", "aarch64", "arm64", "unset"),
        multi=False,
    )

    variant(
        "target_compiler",
        values=compilers,
        description="Compiler suite for building runtime libraries and "
        "generated code on CHPL_TARGET_PLATFORM",
        default="unset",
    )

    variant(
        "target_platform",
        description="Target platform for cross compilation",
        default="unset",
        values=platform_opts,
        multi=False,
    )

    variant(
        "tasks",
        description="Select tasking layer for intra-locale parallelism",
        default="qthreads",
        values=("fifo", "qthreads"),
        multi=False,
    )

    variant(
        "timers",
        description="Select timers implementation",
        default="unset",
        values=("generic", "unset"),
        multi=False,
    )

    variant(
        "unwind",
        description="Build with unwind library for stack tracing",
        default="none",
        values=("bundled", "none", "system"),
    )

    # Deprecated as of (?)
    # variant(
    #     "aux_filesys",
    #     description="Build with runtime support for certain filesystems",
    #     default="none",
    #     values=("none", "lustre", "hdfs"),
    #     multi=False,
    # )

    # This variant is superseded by the host_mem variant
    # TODO: determine what version introduced the host_mem variant and
    # remove this one if it is old enough that all supported versions have host_mem
    # variant(
    #     "mem",
    #     values=("cstdlib", "jemalloc"),
    #     default="jemalloc",
    #     description="Memory management layer",
    #     multi=False,
    # )

    # TODO: for CHPL_X_CC and CHPL_X_CXX, can we capture an arbitrary path, possibly
    # with arguments?
    chpl_env_vars = [
        "CHPL_ATOMICS",
        "CHPL_AUX_FILESYS",
        "CHPL_COMM",
        "CHPL_COMM_SUBSTRATE",
        "CHPL_DEVELOPER",
        "CHPL_GASNET_SEGMENT",
        "CHPL_GMP",
        "CHPL_GPU",
        "CHPL_GPU_ARCH",
        "CHPL_GPU_MEM_STRATEGY",
        "CHPL_HOST_ARCH",
        # "CHPL_HOST_CC",
        "CHPL_HOST_COMPILER",
        # "CHPL_HOST_CXX",
        "CHPL_HOST_JEMALLOC",
        "CHPL_HOST_MEM",
        "CHPL_HOST_PLATFORM",
        "CHPL_HWLOC",
        "CHPL_LAUNCHER",
        "CHPL_LIB_PIC",
        "CHPL_LIBFABRIC",
        "CHPL_LLVM",
        "CHPL_LLVM_CONFIG",
        "CHPL_LLVM_SUPPORT",
        "CHPL_LLVM_VERSION",
        "CHPL_LOCALE_MODEL",
        "CHPL_MEM",
        "CHPL_RE2",
        "CHPL_SANITIZE",
        "CHPL_SANITIZE_EXE",
        "CHPL_TARGET_ARCH",
        # "CHPL_TARGET_CC",
        "CHPL_TARGET_COMPILER",
        "CHPL_TARGET_CPU",
        # "CHPL_TARGET_CXX",
        "CHPL_TARGET_PLATFORM",
        "CHPL_TASKS",
        "CHPL_TIMERS",
        "CHPL_UNWIND",
    ]

    conflicts("platform=windows")  # Support for windows is through WSL only

    conflicts("rocm", when="cuda", msg="Chapel must be built with either CUDA or ROCm, not both")

    conflicts(
        "chpldoc",
        when="@:1.34.0",
        msg="chpldoc has no effect and is installed by default on versions prior to 1.34.0",
    )

    with when("llvm=none"):
        conflicts("cuda", msg="Cuda support requires building with LLVM")
        conflicts("rocm", msg="ROCm support requires building with LLVM")

    # Based on docs https://chapel-lang.org/docs/technotes/gpu.html#requirements
    requires("llvm=bundled", when="^cuda@12:")

    # Add dependencies

    # TODO: Make conditional on +chpldoc variant once removed from install target
    depends_on("doxygen@1.8.17:", when="+chpldoc")

    for opt, dep in package_module_dict.items():
        depends_on(dep, when="package_modules={0}".format(opt), type=("run", "build", "link"))
        depends_on(dep, when="package_modules=all", type=("run", "build", "link"))

    # TODO: llvm version requirements when llvm=system, these are conditional
    # on the version of Chapel

    depends_on("llvm@14:16", when="llvm=spack")

    depends_on("llvm@15", when="llvm=spack ^cuda@12:")

    depends_on("m4")

    with when("developer=True"):
        depends_on("flex")
        depends_on("bison")
        depends_on("tmux")

    depends_on("gmp", when="gmp=spack", type=("build", "link", "run"))

    depends_on("python@3.7:")
    depends_on("cmake@3.16:")

    def unset_chpl_env_vars(self, env):
        # Clean the environment from any pre-set CHPL_ variables that affect the build
        for var in self.chpl_env_vars:
            env.unset(var)

    def configure(self, spec, prefix):
        configure("--prefix={0}".format(prefix))

    def build(self, spec, prefix):
        make()
        if spec.variants["chpldoc"].value:
            make("chpldoc")

    def setup_chpl_compilers(self, env):
        if self.compiler_map.get(self.spec.compiler.name) is None:
            raise InstallError(
                "Chapel did not recognize the {0} compiler".format(self.spec.compiler.name)
            )
        env.set("CHPL_HOST_COMPILER", self.compiler_map[self.spec.compiler.name])
        env.set("CHPL_TARGET_COMPILER", self.compiler_map[self.spec.compiler.name])

    def setup_chpl_comm(self, env, spec):
        env.set("CHPL_COMM", spec.variants["comm"].value)
        if spec.variants["comm_substrate"].value != "none":
            env.set("CHPL_COMM_SUBSTRATE", spec.variants["comm_substrate"].value)

    def setup_chpl_llvm(self, env):
        if self.spec.variants["llvm"].value == "spack":
            env.set(
                "CHPL_LLVM_CONFIG", "{0}/{1}".format(self.spec["llvm"].prefix, "bin/llvm-config")
            )
            env.set("CHPL_LLVM", "system")
        else:
            env.set("CHPL_LLVM", self.spec.variants["llvm"].value)

    def setup_if_not_unset(self, env, var, value):
        if value != "unset":
            if value == "spack":
                value = "system"
            env.set(var, value)

    def setup_env_vars(self, env):
        for v in self.spec.variants.keys():
            self.setup_if_not_unset(env, "CHPL_" + v.upper(), self.spec.variants[v].value)
        self.setup_chpl_llvm(env)
        self.setup_chpl_compilers(env)

        # TODO: a function to set defaults for things where we removed variants
        env.set("CHPL_LOCALE_MODEL", "flat")

        if self.spec.variants["gmp"].value == "spack":
            env.set("CHPL_GMP", "system")
            # TODO: why must we add to CPATH to find gmp.h
            # TODO: why must we add to LIBRARY_PATH to find lgmp
            env.prepend_path("CPATH", self.spec["gmp"].prefix.include)
            env.prepend_path("LIBRARY_PATH", self.spec["gmp"].prefix.lib)
        else:
            env.set("CHPL_GMP", self.spec.variants["gmp"].value)

        if "yaml" in self.get_package_modules:
            env.prepend_path("PKG_CONFIG_PATH", self.spec["libyaml"].prefix.lib.pkgconfig)
            env.prepend_path("CPATH", self.spec["libyaml"].prefix.include)

        if "zmq" in self.get_package_modules:
            env.prepend_path("CPATH", self.spec["libzmq"].prefix.include)
            env.prepend_path("LD_LIBRARY_PATH", self.spec["libzmq"].prefix.lib)
            env.prepend_path("PKG_CONFIG_PATH", self.spec["libzmq"].prefix.lib.pkgconfig)
            env.prepend_path("PKG_CONFIG_PATH", self.spec["libsodium"].prefix.lib.pkgconfig)

        if "curl" in self.get_package_modules:
            env.prepend_path("CPATH", self.spec["curl"].prefix.include)
            env.prepend_path("LD_LIBRARY_PATH", self.spec["curl"].prefix.lib)
            env.prepend_path("PKG_CONFIG_PATH", self.spec["curl"].prefix.lib.pkgconfig)

        if self.spec.variants["cuda"].value:
            # TODO: why must we add to LD_LIBRARY_PATH to find libcudart?
            env.prepend_path("LD_LIBRARY_PATH", self.spec["cuda"].prefix.lib64)
            env.set("CHPL_LOCALE_MODEL", "gpu")
            env.set("CHPL_GPU", "nvidia")
            env.set("CHPL_TARGET_COMPILER", "llvm")

        if self.spec.variants["rocm"].value:
            env.set("CHPL_LOCALE_MODEL", "gpu")
            env.set("CHPL_GPU", "amd")
            env.set("CHPL_TARGET_COMPILER", "llvm")
            env.set("CHPL_HOST_COMPILER", "llvm")
            env.set("CHPL_GPU_ARCH", self.spec.variants["amdgpu_target"].value[0])
            env.set(
                "CHPL_LLVM_CONFIG",
                "{0}/{1}".format(self.spec["llvm-amdgpu"].prefix, "bin/llvm-config"),
            )
            env.prepend_path("CPATH", self.spec["hip"].prefix.include)
            env.set("CHPL_ROCM_PATH", self.spec["llvm-amdgpu"].prefix)
            env.prepend_path("LIBRARY_PATH", self.spec["hip"].prefix.lib)
            env.prepend_path("LIBRARY_PATH", self.spec["hsa-rocr-dev"].prefix.lib)
            env.prepend_path("LD_LIBRARY_PATH", self.spec["hip"].prefix.lib)
            env.prepend_path("LD_LIBRARY_PATH", self.spec["hsa-rocr-dev"].prefix.lib)
        self.setup_chpl_comm(env, self.spec)

    def setup_build_environment(self, env):
        self.unset_chpl_env_vars(env)
        self.setup_env_vars(env)

    def setup_run_environment(self, env):
        self.setup_env_vars(env)
        env.prepend_path(
            "PATH", join_path(self.prefix.share, "chapel", self._output_version_short, "util")
        )

    @property
    @llnl.util.lang.memoized
    def get_package_modules(self):
        test_modules = set()
        for module in self.spec.variants["package_modules"].value:
            if module == "all":
                for m in self.package_module_dict.keys():
                    test_modules.add(m)
            elif module != "none":
                test_modules.add(module)
        return test_modules

    @property
    @llnl.util.lang.memoized
    def _output_version_long(self):
        if str(self.spec.version).lower() == "main":
            return "1.34.0"
        spec_vers_str = str(self.spec.version.up_to(3))
        return spec_vers_str

    @property
    @llnl.util.lang.memoized
    def _output_version_short(self):
        if str(self.spec.version).lower() == "main":
            return "1.34"
        spec_vers_str = str(self.spec.version.up_to(2))
        return spec_vers_str

    def run_test_version(self):
        """Perform version checks on selected installed package binaries."""
        expected = f"version {self._output_version_long}"
        exes = ["chpl"]

        if self.spec.variants["chpldoc"].value:
            exes.append("chpldoc")

        for exe in exes:
            reason = f"ensure version of {exe} is {self._output_version_long}"
            with test_part(self, f"test_version_{exe}", purpose=reason):
                path = join_path(self.prefix.bin, exe)
                if not os.path.isfile(path):
                    raise SkipTest(f"{path} is not installed")
                prog = which(path)
                if "main" in str(self.spec.version):
                    print("skipping detailed version check for main branch")
                    prog("--version", output=str.split, error=str.split)
                    assert prog.returncode == 0
                else:
                    output = prog("--version", output=str.split, error=str.split)
                    assert expected in output

    def run_local_make_check_with_gasnet(self):
        """Setup env to run self-test after installing the package with gasnet"""
        with set_env(
            GASNET_SPAWNFN="L",
            GASNET_QUIET="yes",
            GASNET_ROUTE_OUTPUT="0",
            QT_AFFINITY="no",
            CHPL_QTHREAD_ENABLE_OVERSUBSCRIPTION="1",
            CHPL_RT_MASTERIP="127.0.0.1",
            CHPL_RT_WORKERIP="127.0.0.0",
            CHPL_LAUNCHER="",
        ):
            make("check")

    def run_local_make_check(self):
        if self.spec.variants["comm"].value != "none":
            self.run_local_make_check_with_gasnet()
        else:
            make("check")

    def check(self):
        path_put_first("PATH", [self.prefix.util])
        make("test")

    def run_test_package_modules(self):
        """Test that the package modules are available"""
        if not self.spec.variants["module_tests"].value:
            print("Skipping module tests as module_tests variant is not set")
            return
        tests_to_run = []
        with working_dir(self.stage.source_path):
            with set_env(CHPL_HOME=self.stage.source_path):
                with test_part(self, "test_package_modules", purpose="test package modules"):
                    if "yaml" in self.get_package_modules:
                        tests_to_run.append("test/library/packages/Yaml/writeAndParse.chpl")
                    if "zmq" in self.get_package_modules:
                        tests_to_run.append("test/library/packages/ZMQ/weather.chpl")
                    if "ssl" in self.get_package_modules:
                        tests_to_run.append("test/library/packages/Crypto/")
                    # TODO: These tests fail with llvm, unable to find C variable CURLPAUSE_CONT
                    if (
                        "curl" in self.get_package_modules
                        and self.spec.variants["llvm"].value == "none"
                    ):
                        with set_env(CHPL_NIGHTLY_TEST_CONFIG_NAME="networking-packages"):
                            print("Running package module test for package 'curl'")
                            res = subprocess.run(
                                ["util/start_test", "test/library/packages/Curl/"]
                            )
                            assert res.returncode == 0
                            print("Running package module test for package 'url'")
                            res = subprocess.run(["util/start_test", "test/library/packages/URL/"])
                            assert res.returncode == 0
                    if "hdf5" in self.get_package_modules:
                        tests_to_run.append("test/library/packages/HDF5/")
                    if "protobuf" in self.get_package_modules:
                        tests_to_run.append("test/library/packages/ProtobufProtocolSupport/")
                    print("Running package module tests for packages...")
                    tests_to_run.insert(0, "util/start_test")
                    res = subprocess.run([t for t in tests_to_run])
                    assert res.returncode == 0

    @run_after("install")
    def self_check(self):
        """Run the self-check after installing the package"""
        path_put_first("PATH", [self.prefix.bin])
        self.run_test_version()
        if self.spec.variants["check"].value:
            with set_env(CHPL_HOME=self.stage.source_path):
                with working_dir(self.stage.source_path):
                    if self.spec.variants["cuda"].value or self.spec.variants["rocm"].value:
                        with set_env(COMP_FLAGS="--no-checks --no-compiler-driver"):
                            self.run_local_make_check()
                    else:  # Not GPU
                        self.run_local_make_check()
                    if self.spec.variants["chpldoc"].value:
                        make("check-chpldoc")
        self.run_test_package_modules()
