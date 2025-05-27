# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import os.path
import pathlib
import platform
import re
import sys
import warnings

from spack_repo.builtin.build_systems.compiler import CompilerPackage
from spack_repo.builtin.build_systems.oneapi import IntelOneApiPackage

from spack_repo.builtin.packages.intel_oneapi_compilers.oneapi_versions import oneAPIVersions

from spack.build_environment import dso_suffix
from spack.package import *

IS_WINDOWS = sys.platform == "win32"


class UnixDebugFlags:
    DEBUG = "-debug"
    G = "-g"
    G0 = "-g0"
    G1 = "-g1"
    G2 = "-g2"
    G3 = "-g3"


class WindowsDebugFlags:
    DEBUG = "/debug"
    G = "/g"
    G0 = "/g0"
    G1 = "/g1"
    G2 = "/g2"
    G3 = "/g3"


class UnixOptFlags:
    O = "-O"
    O0 = "-O0"
    O1 = "-O1"
    O2 = "-O2"
    O3 = "-O3"
    OFAST = "-Ofast"
    OS = "-Os"


class WindowsOptFlags:
    O = "/O"
    O0 = "/O0"
    O1 = "/O1"
    O2 = "/O2"
    O3 = "/O3"
    OFAST = "/Ofast"
    OS = "/Os"


if IS_WINDOWS:
    DebugFlags = WindowsDebugFlags
    OptFlags = WindowsOptFlags
else:
    DebugFlags = UnixDebugFlags
    OptFlags = UnixOptFlags


@IntelOneApiPackage.update_description
class IntelOneapiCompilers(IntelOneApiPackage, CompilerPackage):
    """Intel oneAPI Compilers. Includes: icx, icpx, ifx, and ifort.
    Releases before 2024.0 include icc/icpc"""

    maintainers("rscohn2")

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi.html"

    compiler_languages = ["c", "cxx", "fortran"]
    c_names = ["icx"]
    cxx_names = ["icpx"]
    fortran_names = ["ifx"]
    compiler_version_argument = "--version" if not IS_WINDOWS else ""
    compiler_version_regex = (
        r"(?:(?:oneAPI DPC\+\+(?:\/C\+\+)? Compiler)|(?:\(IFORT\))|(?:\(IFX\))) (\S+)"
    )

    debug_flags = [DebugFlags.DEBUG, DebugFlags.G, DebugFlags.G0, DebugFlags.G1, DebugFlags.G2, DebugFlags.G3]
    opt_flags = [OptFlags.O, OptFlags.O0, OptFlags.O1, OptFlags.O2, OptFlags.O3, OptFlags.OFAST, OptFlags.OS]

    openmp_flag = "-fiopenmp"

    compiler_wrapper_link_paths = {
        "c": os.path.join("oneapi", "icx"),
        "cxx": os.path.join("oneapi", "icpx"),
        "fortran": os.path.join("oneapi", "ifx"),
    }

    implicit_rpath_libs = [
        "libirc",
        "libifcore",
        "libifcoremt",
        "libirng",
        "libsvml",
        "libintlc",
        "libimf",
        "libsycl",
        "libOpenCL",
    ]

    stdcxx_libs = ("-cxxlib",)

    oneAPIVersions.generate_versions()

    provides("c", "cxx")
    provides("fortran")

    def _standard_flag(self, *, language, standard):
        flags = {
            "cxx": {
                "11": "-std=c++11",
                "14": "-std=c++14",
                "17": "-std=c++17",
                "20": "-std=c++20",
            },
            "c": {"99": "-std=c99", "11": "-std=c1x"},
        }
        return flags[language][standard]

    with when(f"platform=linux"):
        # See https://github.com/spack/spack/issues/39252
        depends_on("patchelf@:0.17", type="build", when="@:2024.1")

        # Disable the variant below for now on Windows for simplicitys sake
        # enable once basic oneAPI functionality is stable 

        # Add the nvidia variant
        variant("nvidia", default=False, description="Install NVIDIA plugin for OneAPI")
        conflicts("@:2022.2.1", when="+nvidia", msg="Codeplay NVIDIA plugin requires newer release")
        # Add the amd variant
        variant("amd", default=False, description="Install AMD plugin for OneAPI")
        conflicts("@:2022.2.1", when="+amd", msg="Codeplay AMD plugin requires newer release")

        depends_on("gcc languages=c,c++", type="run")

    with when("platform=windows"):
        depends_on("msvc", type="run")

    @property
    def v2_layout_versions(self):
        return "@2024:"

    @property
    def component_dir(self):
        return "compiler"

    @property
    def _llvm_bin(self):
        return self.component_prefix.bin if self.v2_layout else self.component_prefix.linux.bin

    @property
    def _classic_bin(self):
        return (
            self.component_prefix.bin
            if self.v2_layout
            else self.component_prefix.linux.bin.intel64
        )

    @property
    def compiler_search_prefix(self):
        return self._llvm_bin

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        """Adds environment variables to the generated module file.

        These environment variables come from running:

        .. code-block:: console

           $ source {prefix}/{component}/{version}/env/vars.sh

        and from setting CC/CXX/F77/FC
        """
        super().setup_run_environment(env)

        # umf is packaged with compiler and not available as a standalone
        if "~envmods" not in self.spec and self.spec.satisfies("@2025:") and not IS_WINDOWS:
            env.extend(
                EnvironmentModifications.from_sourcing_file(
                    self.prefix.umf.latest.env.join("vars.sh"), *self.env_script_args
                )
            )

        env.set("CC", self._llvm_bin.icx)
        env.set("CXX", self._llvm_bin.icpx)
        env.set("F77", self._llvm_bin.ifx)
        env.set("FC", self._llvm_bin.ifx)

    def setup_dependent_build_environment(
        self, env: EnvironmentModifications, dependent_spec: Spec
    ) -> None:
        super().setup_dependent_build_environment(env, dependent_spec)
        # workaround bug in icpx driver where it requires sycl-post-link is on the PATH
        # It is located in the same directory as the driver. Error message:
        #   clang++: error: unable to execute command:
        #   Executable "sycl-post-link" doesn't exist!
        # also ensures that shared objects and libraries required by the compiler,
        # e.g. libonnx, can be found succesfully
        # due to a fix, this is no longer required for OneAPI versions >= 2024.2
        if self.cxx and self.spec.satisfies("%oneapi@:2024.1"):
            bin_dir = os.path.dirname(self.cxx)
            lib_dir = os.path.join(os.path.dirname(bin_dir), "lib")
            env.prepend_path("PATH", bin_dir)
            env.prepend_path("LD_LIBRARY_PATH", lib_dir)

        # 2024 release bumped the libsycl version because of an ABI
        # change, 2024 compilers are required.  You will see this
        # error:
        #
        # /usr/bin/ld: warning: libsycl.so.7, needed by ...., not found
        if self.spec.satisfies("%oneapi@:2023"):
            for c in ["dnn"]:
                if self.spec.satisfies(f"^intel-oneapi-{c}@2024:"):
                    warnings.warn(f"intel-oneapi-{c}@2024 SYCL APIs requires %oneapi@2024:")

    def install(self, spec, prefix):
        # Copy instead of install to speed up debugging
        # install_tree("/opt/intel/oneapi/compiler", self.prefix)
        # return

        # install cpp
        super().install(spec, prefix)

        # install fortran
        ftn = find("fortran-installer", "*")
        if ftn:
            self.install_component(ftn[0])

            # Some installers have a bug and do not return an error code when failing
            if not is_exe(self._llvm_bin.ifx):
                raise RuntimeError("Fortran install failed")
        # install nvidia-plugin
        if self.spec.satisfies("+nvidia"):
            nvidia_script = find("nvidia-plugin-installer", "*")
            if nvidia_script:
                if platform.system() == "Linux":
                    bash = Executable("bash")
                    # For NVIDIA plugin installer
                    bash(nvidia_script[0], "-y", "--install-dir", self.prefix)
                elif IS_WINDOWS:
                    Executable(nvidia_script[0])("-a", "-y", "--install-dir", self.prefix)
        if self.spec.satisfies("+amd"):
            amd_script = find("amd-plugin-installer", "*")
            if amd_script:
                if platform.system() == "Linux":
                    bash = Executable("bash")
                    # For AMD plugin installer
                    bash(amd_script[0], "-y", "--install-dir", self.prefix)
                elif IS_WINDOWS:
                    Executable(amd_script[0])("-a", "-y", "--install-dir", self.prefix)

    @run_after("install", when="platform=linux")
    def inject_rpaths(self):
        # The oneapi compilers cannot find their own internal shared
        # libraries. If you are using an externally installed oneapi,
        # then you need to source setvars.sh, which will set
        # LD_LIBRARY_PATH. If you are using spack to install the
        # compilers, then we patch the binaries that have this
        # problem. Over time, intel has corrected most of the
        # issues. I am using the 2024 release as a milestone to stop
        # patching everything and just patching the binaries that have
        # a problem.

        # 2024.2 no longer needs patching
        if self.spec.satisfies("@2024.2:"):
            return

        # 2024 fixed all but these 2
        patchelf = which("patchelf")
        if self.spec.satisfies("@2024:"):
            patchelf.add_default_arg("--set-rpath", self.component_prefix.lib)
            patchelf(self.component_prefix.bin.join("sycl-post-link"))
            patchelf(self.component_prefix.bin.compiler.join("llvm-spirv"))
            return

        # Sets rpath so the compilers can work without setting LD_LIBRARY_PATH.
        patchelf.add_default_arg("--set-rpath", ":".join(self._ld_library_path()))
        for pd in ["bin", "lib", join_path("compiler", "lib", "intel64_lin")]:
            for file in find(self.component_prefix.linux.join(pd), "*", recursive=False):
                # Try to patch all files, patchelf will do nothing and fail if file
                # should not be patched
                patchelf(file, fail_on_error=False)

    def write_config_file(self, flags, path, compilers):
        for compiler in compilers:
            # Tolerate missing compilers.
            # Initially, we installed icx/ifx/icc/ifort into a single prefix.
            # Starting in 2024, there is no icc. 2023.2.3 does not have an ifx.
            if os.path.exists(path.join(compiler)):
                p = path.join(compiler + ".cfg")
                with open(p, "w") as f:
                    f.write(" ".join(flags))
                set_install_permissions(p)

    @run_after("install", when="platform=linux")
    def extend_config_flags(self):
        # Extends compiler config files to inject additional compiler flags.

        # Inject rpath flags to the runtime libraries.
        # TODO: this uses a static string for the rpath argument, but should actually
        #  make sure that it matches the cc_rpath_arg etc. arguments defined in
        #  spack.compilers.oneapi and spack.compilers.intel (for now, these are
        #  inherited from spack.compilers.compiler.Compiler): these can theoretically be
        #  different for different compiler versions and for different languages (C,
        #  C++, and Fortran), but in practice are not.
        # TODO: it is unclear whether we should really use all elements of
        #  _ld_library_path because it looks like the only rpath that needs to be
        #  injected is self.component_prefix.linux.compiler.lib.intel64_lin.
        if self.v2_layout:
            common_flags = ["-Wl,-rpath,{}".format(self.component_prefix.lib)]
        else:
            common_flags = ["-Wl,-rpath,{}".format(d) for d in self._ld_library_path()]

        # Make sure that underlying clang gets the right GCC toolchain by default
        gcc = self.spec["gcc"].package
        llvm_flags = [f"--gcc-toolchain={gcc.prefix}"]
        classic_flags = [f"-gcc-name={gcc.cc}", f"-gxx-name={gcc.cxx}"]

        # Older versions trigger -Wunused-command-line-argument warnings whenever
        # linker flags are passed in preprocessor (-E) or compilation mode (-c).
        # The cfg flags are treated as command line flags apparently. Newer versions
        # do not trigger these warnings. In some build systems these warnings can
        # cause feature detection to fail, so we silence them with -Wno-unused-...
        if self.spec.satisfies("@:2022.0"):
            llvm_flags.append("-Wno-unused-command-line-argument")

        self.write_config_file(common_flags + llvm_flags, self._llvm_bin, ["icx", "icpx"])
        self.write_config_file(
            common_flags + (llvm_flags if self.spec.satisfies("@2022.1.0:") else classic_flags),
            self._llvm_bin,
            ["ifx"],
        )
        self.write_config_file(common_flags + classic_flags, self._classic_bin, ["ifort"])
        self.write_config_file(common_flags + classic_flags, self._classic_bin, ["icc", "icpc"])

    def _ld_library_path(self):
        # Returns an iterable of directories that might contain shared runtime libraries
        # of the compilers themselves and the executables they produce.
        for d in [
            "lib",
            join_path("lib", "x64"),
            join_path("lib", "emu"),
            join_path("lib", "oclfpga", "host", "linux64", "lib"),
            join_path("lib", "oclfpga", "linux64", "lib"),
            join_path("compiler", "lib", "intel64_lin"),
            join_path("compiler", "lib"),
        ]:
            p = join_path(self.component_prefix.linux, d)
            if find(p, "*." + dso_suffix, recursive=False):
                yield p

    def archspec_name(self):
        return "oneapi"

    @classmethod
    def determine_version(cls, exe):
        if not IS_WINDOWS:
            return super().determine_version(exe)
        else:
            # Intel compilers on Windows do not have a proper version argument
            # Errors out and prints version info with no args
            match = re.search(
                cls.compiler_version_regex,
                spack.build_systems.compiler.compiler_output(
                    exe, version_argument=None, ignore_errors=(1,)
                ),
            )
            if match:
                return match.group(1)

    @classmethod
    def determine_variants(cls, exes, version_str):
        variant, extra_attributes = super().determine_variants(exes, version_str)

        bin_dirs = {pathlib.Path(x).parent for x in exes}
        if len(bin_dirs) != 1:
            dirs = ", ".join([str(x) for x in sorted(bin_dirs)])
            raise RuntimeError(f"executables found in multiple dirs: {dirs}")
        bin_dir = bin_dirs.pop()

        # Some sites symlink the bindir to the top level of the prefix
        if "compiler" in bin_dir.parts:
            # Normal installation
            prefix_parts = bin_dir.parts[: bin_dir.parts.index("compiler")]
        else:
            # Executables from top level bin dir as symlinks
            prefix_parts = bin_dir.parts[:-1]

        computed_prefix = pathlib.Path(*prefix_parts)
        extra_attributes["prefix"] = str(computed_prefix)

        return variant, extra_attributes

    @classmethod
    def runtime_constraints(cls, *, spec, pkg):
        for language in ("c", "cxx", "fortran"):
            pkg("*").depends_on(
                f"intel-oneapi-runtime@{spec.version}:",
                when=f"%[virtuals={language}] {spec.name}@{spec.versions}",
                type="link",
                description="Inject intel-oneapi-runtime when oneapi is used as "
                f"a {language} compiler",
            )

        for fortran_virtual in ("fortran-rt", "libifcore@5"):
            pkg("*").depends_on(
                fortran_virtual,
                when=f"%[virtuals=fortran] {spec.name}@{spec.versions}",
                type="link",
                description="Add a dependency on 'libifcore' for nodes compiled with "
                f"{spec.name}@{spec.versions} and using the 'fortran' language",
            )
        # The version of intel-oneapi-runtime is the same as the %oneapi used to "compile" it
        pkg("intel-oneapi-runtime").requires(
            f"@{spec.versions}", when=f"%{spec.name}@{spec.versions}"
        )

        # If a node used %intel-oneapi-runtime@X.Y its dependencies must use @:X.Y
        # (technically @:X is broader than ... <= @=X but this should work in practice)
        pkg("*").propagate(
            f"intel-oneapi-compilers@:{spec.version}", when=f"%{spec.name}@{spec.versions}"
        )

    def _cc_path(self):
        return str(self._llvm_bin.icx)

    def _cxx_path(self):
        return str(self._llvm_bin.icpx)

    def _fortran_path(self):
        return str(self._llvm_bin.ifx)