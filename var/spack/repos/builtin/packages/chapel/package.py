# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import subprocess

from spack.package import *
from spack.util.environment import set_env


@llnl.util.lang.memoized
def is_CrayEX():
    # Credit to upcxx package for this hpe-cray-ex detection function
    if spack.platforms.host().name == "linux":
        target = os.environ.get("CRAYPE_NETWORK_TARGET")
        if target in ["ofi", "ucx"]:  # normal case
            return True
        elif target is None:  # but some systems lack Cray PrgEnv
            fi_info = which("fi_info")
            if (
                fi_info
                and fi_info("-l", output=str, error=str, fail_on_error=False).find("cxi") >= 0
            ):
                return True
    return False


class Chapel(AutotoolsPackage, CudaPackage, ROCmPackage):
    """Chapel is a modern programming language that is parallel, productive,
    portable, scalable and open-source. The Chapel package comes with many
    options in the form of variants, most of which can be left unset to allow
    Chapel's built-in scripts to determine the proper values based on the environment."""

    homepage = "https://chapel-lang.org/"

    url = "https://github.com/chapel-lang/chapel/archive/refs/tags/2.0.0.tar.gz"
    git = "https://github.com/chapel-lang/chapel.git"

    test_requires_compiler = True

    executables = ["^chpl$", "^chpldoc$"]

    # A list of GitHub accounts to notify when the package is updated.
    # TODO: add chapel-project github account
    maintainers("arezaii", "bonachea")

    # See https://spdx.org/licenses/ for a list.
    license("Apache-2.0")

    version("main", branch="main")

    version("2.0.1", sha256="47e1f3789478ea870bd4ecdf52acbe469d171b89b663309325431f3da7c75008")
    version("2.0.0", sha256="a8cab99fd034c7b7229be8d4626ec95cf02072646fb148c74b4f48c460c6059c")

    patch("fix_spack_cc_wrapper_in_cray_prgenv.patch", when="@2.0.0:")

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
        "llvm": "llvm",
        "oneapi": "intel",
        "pgi": "pgi",
        "rocmcc": "clang",
        "unset": "unset",
    }

    cpu_options = (
        "native",
        "none",
        "unknown",
        "unset",
        "aarch64",
        "barcelona",
        "bdver1",
        "bdver2",
        "bdver3",
        "bdver4",
        "broadwell",
        "core2",
        "haswell",
        "ivybridge",
        "k8",
        "k8sse3",
        "nehalem",
        "sandybridge",
        "skylake",
        "thunderx",
        "thunderx2t99",
        "westmere",
    )

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

    # TODO: refactor this somehow, this is a separate documentation tool, not a variant of chapel
    variant("chpldoc", default=False, description="Build chpldoc in addition to chpl")

    variant(
        "comm",
        default="none",
        description="Build Chapel with multi-locale support",
        values=("gasnet", "none", "ofi", "ugni"),
    )

    variant(
        "comm_substrate",
        default="unset",
        description="Build Chapel with GASNet multi-locale support using the "
        "supplied CHPL_COMM_SUBSTRATE",
        values=("ibv", "ofi", "udp", "unset"),
        multi=False,
        sticky=True,  # never allow the concretizer to choose this
    )

    # Chapel depends on GASNet whenever comm=gasnet.
    # The default (and recommendation) is to use the embedded copy of GASNet.
    # This variant allows overriding with a particular version of GASNet sources,
    # although this is not officially supported and some combinations might be rejected.
    variant(
        "gasnet",
        description="Control the GASNet library version used",
        default="bundled",
        values=("bundled", "spack"),
        multi=False,
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

    # Feedback that it's hard to imagine any circumstance where host_compiler or
    # target_compiler could meaningfully differ from what Spack already knows about
    # variant(
    #     "host_compiler",
    #     values=compilers,
    #     description="Compiler suite for building the Chapel compiler on CHPL_HOST_PLATFORM",
    #     default="unset",
    # )

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
        values=("bundled", "none", "spack"),
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
        "package_modules",
        description="Include package module dependencies with spack",
        values=disjoint_sets(("none",), ("all",), package_module_dict.keys())
        .with_error("'none' or 'all' cannot be activated along with other package_modules")
        .with_default("all")
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

    # Feedback that it's hard to imagine any circumstance where host_compiler or
    # target_compiler could meaningfully differ from what Spack already knows about
    # variant(
    #     "target_compiler",
    #     values=compilers,
    #     description="Compiler suite for building runtime libraries and "
    #     "generated code on CHPL_TARGET_PLATFORM",
    #     default="unset",
    # )

    variant(
        "target_cpu",
        values=cpu_options,
        description="Indicate that the target executable should be specialized "
        "to the given architecture when using --specialize (and --fast).",
        default="unset",
        multi=False,
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
        multi=False,
    )

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
    conflicts("rocm", when="@:2.0.0", msg="ROCm support in spack requires Chapel 2.0.0 or later")

    conflicts(
        "comm_substrate=unset",
        when="comm=gasnet",
        msg="comm=gasnet requires you to also set comm_substrate= to the appropriate network",
    )

    conflicts(
        "^python@3.12:",
        when="@:2.1.0",
        msg="Chapel versions prior to 2.1.0 may produce SyntaxWarnings with Python >= 3.12",
    )

    with when("llvm=none"):
        conflicts("cuda", msg="Cuda support requires building with LLVM")
        conflicts("rocm", msg="ROCm support requires building with LLVM")

    # Add dependencies

    depends_on("doxygen@1.8.17:", when="+chpldoc")

    for opt, dep in package_module_dict.items():
        depends_on(dep, when="package_modules={0}".format(opt), type=("run", "build", "link"))
        depends_on(dep, when="package_modules=all", type=("run", "build", "link"))

    # TODO: llvm version requirements when llvm=system, these are conditional
    # on the version of Chapel

    depends_on("llvm@14:17", when="llvm=spack")

    # Based on docs https://chapel-lang.org/docs/technotes/gpu.html#requirements
    depends_on("llvm@16:", when="llvm=spack ^cuda@12:")
    requires(
        "^llvm targets=all",
        msg="llvm=spack +cuda requires LLVM support the nvptx target",
        when="llvm=spack +cuda",
    )

    depends_on("cuda@11:", when="+cuda", type=("build", "link", "run", "test"));

    # This is because certain systems have binutils installed as a system package
    # but do not include the headers. Spack incorrectly supplies those external
    # packages as proper dependencies for LLVM, but then LLVM will fail to build
    # with an error about missing plugin-api.h
    depends_on("binutils+gold+ld+plugins+headers", when="llvm=bundled")

    depends_on("m4")

    depends_on("gmp", when="gmp=spack", type=("build", "link", "run"))
    depends_on("hwloc", when="hwloc=spack", type=("build", "link", "run", "test"))

    depends_on("gasnet conduits=none", when="gasnet=spack")

    depends_on("python@3.7:")
    depends_on("cmake@3.16:")

    def unset_chpl_env_vars(self, env):
        # Clean the environment from any pre-set CHPL_ variables that affect the build
        for var in self.chpl_env_vars:
            env.unset(var)

    def configure(self, spec, prefix):
        self.setup_gasnet()
        configure("--prefix={0}".format(prefix))

    def build(self, spec, prefix):
        make()
        if spec.variants["chpldoc"].value:
            make("chpldoc")

    def setup_chpl_platform(self, env):
        if self.spec.variants["host_platform"].value == "unset":
            if is_CrayEX():
                env.set("CHPL_HOST_PLATFORM", "hpe-cray-ex")

    def setup_chpl_compilers(self, env):
        if self.compiler_map.get(self.spec.compiler.name) is None:
            raise InstallError(
                "Chapel did not recognize the {0} compiler".format(self.spec.compiler.name)
            )
        env.set("CHPL_HOST_COMPILER", self.compiler_map[self.spec.compiler.name])
        env.set("CHPL_TARGET_COMPILER", self.compiler_map[self.spec.compiler.name])

        # Undo spack compiler wrappers:
        # the C/C++ compilers must work post-install
        if is_CrayEX() and os.environ.get("CRAYPE_DIR"):
            real_cc = join_path(os.environ["CRAYPE_DIR"], "bin", "cc")
            real_cxx = join_path(os.environ["CRAYPE_DIR"], "bin", "CC")
        else:
            real_cc = self.compiler.cc
            real_cxx = self.compiler.cxx
        env.set("CHPL_TARGET_CC", real_cc)
        env.set("CHPL_TARGET_CXX", real_cxx)

    def setup_chpl_comm(self, env, spec):
        env.set("CHPL_COMM", spec.variants["comm"].value)

    def setup_gasnet(self):
        if self.spec.variants["gasnet"].value == "spack":
            dst = join_path(self.stage.source_path, "third-party", "gasnet", "gasnet-src")
            remove_directory_contents(dst)
            os.rmdir(dst)
            symlink(self.spec["gasnet"].prefix.src, dst)

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

    def prepend_cpath_include(self, env, prefix):
        if prefix != "/usr":
            env.prepend_path("CPATH", prefix.include)

    def setup_env_vars(self, env):
        for v in self.spec.variants.keys():
            self.setup_if_not_unset(env, "CHPL_" + v.upper(), self.spec.variants[v].value)
        self.setup_chpl_llvm(env)
        self.setup_chpl_compilers(env)
        self.setup_chpl_platform(env)

        # TODO: a function to set defaults for things where we removed variants
        # We'll set to GPU later if +rocm or +cuda requested
        env.set("CHPL_LOCALE_MODEL", "flat")

        if self.spec.variants["gmp"].value == "spack":
            env.set("CHPL_GMP", "system")
            # TODO: why must we add to CPATH to find gmp.h
            # TODO: why must we add to LIBRARY_PATH to find lgmp
            self.prepend_cpath_include(env, self.spec["gmp"].prefix)
            env.prepend_path("LIBRARY_PATH", self.spec["gmp"].prefix.lib)
        else:
            env.set("CHPL_GMP", self.spec.variants["gmp"].value)

        if "yaml" in self.get_package_modules:
            env.prepend_path("PKG_CONFIG_PATH", self.spec["libyaml"].prefix.lib.pkgconfig)
            self.prepend_cpath_include(env, self.spec["libyaml"].prefix)

        if "zmq" in self.get_package_modules:
            self.prepend_cpath_include(env, self.spec["libzmq"].prefix)
            env.prepend_path("LD_LIBRARY_PATH", self.spec["libzmq"].prefix.lib)
            env.prepend_path("PKG_CONFIG_PATH", self.spec["libzmq"].prefix.lib.pkgconfig)
            env.prepend_path("PKG_CONFIG_PATH", self.spec["libsodium"].prefix.lib.pkgconfig)

        if "curl" in self.get_package_modules:
            self.prepend_cpath_include(env, self.spec["curl"].prefix)
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
            self.prepend_cpath_include(env, self.spec["hip"].prefix)
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
            return "2.1.0"
        spec_vers_str = str(self.spec.version.up_to(3))
        return spec_vers_str

    @property
    @llnl.util.lang.memoized
    def _output_version_short(self):
        if str(self.spec.version).lower() == "main":
            return "2.1"
        spec_vers_str = str(self.spec.version.up_to(2))
        return spec_vers_str

    def test_version(self):
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
                if prog is None:
                    raise RuntimeError(f"Could not find {path}")
                output = prog("--version", output=str.split, error=str.split)
                assert expected in output

    def check(self):
        # TODO: This is here because it's hard to have our make test target work
        # with the spack test framework. Our make test target relies on using
        # `start_test` and it really expects to be ran from the source directory
        # but spack creates a test cache directory and runs the tests from there.
        # we could conceivably just copy most everything over to the cache directory,
        # but the other issue is that these tests take a long time to run and
        # it's not likely users are going to want to wait 30 minutes or maybe some
        # number of hours for the tests to run. So we're going to skip this for now
        # and just rely on minimal hello world and version number tests.
        # We can't just run make check here because chpl isn't yet installed
        # and we need it to be in the PATH for make check to work
        pass

    def check_chpl_install_gasnet(self):
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
            return subprocess.run(["util/test/checkChplInstall"])

    def check_chpl_install(self):
        if self.spec.variants["comm"].value != "none":
            return self.check_chpl_install_gasnet()
        else:
            return subprocess.run(["util/test/checkChplInstall"])

    def test_hello(self):
        """Run the hello world test"""
        with working_dir(self.test_suite.current_test_cache_dir):
            with set_env(CHPL_CHECK_HOME=self.test_suite.current_test_cache_dir):
                with test_part(self, "test_hello", purpose="test hello world"):
                    if self.spec.variants["cuda"].value or self.spec.variants["rocm"].value:
                        with set_env(COMP_FLAGS="--no-checks --no-compiler-driver"):
                            res = self.check_chpl_install()
                            assert res and res.returncode == 0
                    else:
                        res = self.check_chpl_install()
                        assert res and res.returncode == 0

    # TODO: This is a pain because the checkChplDoc script doesn't have the same
    # support for CHPL_CHECK_HOME and chpldoc is finicky about CHPL_HOME
    def test_chpldoc(self):
        """Run the chpldoc test"""
        if not self.spec.variants["chpldoc"].value:
            print("Skipping chpldoc test as chpldoc variant is not set")
            return
        with working_dir(self.test_suite.current_test_cache_dir):
            with set_env(CHPL_HOME=self.test_suite.current_test_cache_dir):
                with test_part(self, "test_chpldoc", purpose="test chpldoc"):
                    res = subprocess.run(["util/test/checkChplDoc"])
                    assert res.returncode == 0

    # TODO: In order to run these tests, there's a lot of infrastructure to copy
    # from the Chapel test suite and there are conflicts with CHPL_HOME needing
    # to match the compiler's directory and the test suite's directory
    # def test_package_modules(self):
    #     """Test that the package modules are available"""
    #     # if not self.spec.variants["module_tests"].value:
    #     #     print("Skipping module tests as module_tests variant is not set")
    #     #     return
    #     tests_to_run = []
    #     with working_dir(self.test_suite.current_test_cache_dir):
    #         with set_env(CHPL_HOME=join_path(self.spec.prefix.share,
    #                      "chapel", self._output_version_short)):
    #             with test_part(self, "test_package_modules", purpose="test package modules"):
    #                 if "yaml" in self.get_package_modules:
    #                     tests_to_run.append("test/library/packages/Yaml/writeAndParse.chpl")
    #                 if "zmq" in self.get_package_modules:
    #                     tests_to_run.append("test/library/packages/ZMQ/weather.chpl")
    #                 if "ssl" in self.get_package_modules:
    #                     tests_to_run.append("test/library/packages/Crypto/")
    #                 # TODO: These tests fail with llvm, unable to find C variable CURLPAUSE_CONT
    #                 if (
    #                     "curl" in self.get_package_modules
    #                     and self.spec.variants["llvm"].value == "none"
    #                 ):
    #                     with set_env(CHPL_NIGHTLY_TEST_CONFIG_NAME="networking-packages"):
    #                         print("Running package module test for package 'curl'")
    #                         res = subprocess.run(
    #                             ["util/start_test", "test/library/packages/Curl/"]
    #                         )
    #                         assert res.returncode == 0
    #                         print("Running package module test for package 'url'")
    #                         res = subprocess.run(["util/start_test",
    #                                               "test/library/packages/URL/"])
    #                         assert res.returncode == 0
    #                 if "hdf5" in self.get_package_modules:
    #                     tests_to_run.append("test/library/packages/HDF5/")
    #                 if "protobuf" in self.get_package_modules:
    #                     tests_to_run.append("test/library/packages/ProtobufProtocolSupport/")
    #                 if len(tests_to_run) > 0:
    #                     with set_env(CHPL_HOME=self.test_suite.current_test_cache_dir):
    #                         compiler = join_path(self.spec.prefix.bin,'chpl')
    #                         print("Running package module tests for packages...")
    #                         print(f" command to run: util/start_test --compiler {compiler}")
    #                         tests_to_run.insert(0, "util/start_test")
    #                         tests_to_run.insert(1, "--compiler")
    #                         tests_to_run.insert(2, compiler)
    #                         res = subprocess.run([t for t in tests_to_run])
    #                         assert res.returncode == 0

    @run_after("install")
    def copy_test_files(self):
        """Copy test files to the install directory"""
        test_files = [
            "test/release/examples",
            "util/start_test",
            "util/test",
            "util/chplenv",
            "util/config",
            #   "test/library/packages/Curl",
            #   "test/library/packages/URL/",
            #   "test/library/packages/ProtobufProtocolSupport/",
            #   "test/library/packages/Crypto/",
            #   "test/library/packages/Yaml/",
            #   "test/library/packages/ZMQ/",
            #   "test/library/packages/HDF5/",
            "chplconfig",
            "make",
            "third-party/chpl-venv/",
        ]
        cache_extra_test_sources(self, test_files)

    # @run_after("install")
    # @on_package_attributes(run_tests=True)
    # def self_check(self):
    #     """Run the self-check after installing the package"""
    #     path_put_first("PATH", [self.prefix.bin])
    #     self.test_version()
    #     with set_env(CHPL_HOME=self.stage.source_path):
    #         with working_dir(self.stage.source_path):
    #             if self.spec.variants["cuda"].value or self.spec.variants["rocm"].value:
    #                 with set_env(COMP_FLAGS="--no-checks --no-compiler-driver"):
    #                     self.run_local_make_check()
    #             else:  # Not GPU
    #                 self.run_local_make_check()
    #             if self.spec.variants["chpldoc"].value:
    #                 make("check-chpldoc")
    #     self.test_package_modules()
