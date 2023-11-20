# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_environment import dso_suffix
from spack.package import *

versions = [
    {
        "version": "2024.0.0",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm//IRC_NAS/5c8e686a-16a7-4866-b585-9cf09e97ef36/l_dpcpp-cpp-compiler_p_2024.0.0.49524_offline.sh",
            "sha256": "d10bad2009c98c631fbb834aae62012548daeefc806265ea567316cd9180a684",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm//IRC_NAS/89b0fcf9-5c00-448a-93a1-5ee4078e008e/l_fortran-compiler_p_2024.0.0.49493_offline.sh",
            "sha256": "57faf854b8388547ee4ef2db387a9f6f3b4d0cebd67b765cf5e844a0a970d1f9",
        },
    },
    {
        "version": "2023.2.1",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm//IRC_NAS/ebf5d9aa-17a7-46a4-b5df-ace004227c0e/l_dpcpp-cpp-compiler_p_2023.2.1.8_offline.sh",
            "sha256": "f5656b2f5bb5d904639e6ef1f90a2d2e760d2906e82ebc0dd387709738ca714b",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm//IRC_NAS/0d65c8d4-f245-4756-80c4-6712b43cf835/l_fortran-compiler_p_2023.2.1.8_offline.sh",
            "sha256": "d4e36abc014c184698fec318a127f15a696b5333b3b0282aba1968b351207185",
        },
    },
    {
        "version": "2023.2.0",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/748687b0-5a22-467c-86c6-c312fa0206b2/l_dpcpp-cpp-compiler_p_2023.2.0.49256_offline.sh",
            "sha256": "21497b2dd2bc874794c2321561af313082725f61e3101e05a050f98b7351e08f",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/237236c4-434b-4576-96ac-020ceeb22619/l_fortran-compiler_p_2023.2.0.49254_offline.sh",
            "sha256": "37c0ad6f0013512d98e385f8708ca29b23c45fddc9ec76069f1d93663668d511",
        },
    },
    {
        "version": "2023.1.0",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/89283df8-c667-47b0-b7e1-c4573e37bd3e/l_dpcpp-cpp-compiler_p_2023.1.0.46347_offline.sh",
            "sha256": "3ac1c1179501a2646cbb052b05426554194573b4f8e2344d7699eed03fbcfa1d",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/150e0430-63df-48a0-8469-ecebff0a1858/l_fortran-compiler_p_2023.1.0.46348_offline.sh",
            "sha256": "7639af4b6c928e9e3ba92297a054f78a55f4f4d0db9db0d144cc6653004e4f24",
        },
    },
    {
        "version": "2023.0.0",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/19123/l_dpcpp-cpp-compiler_p_2023.0.0.25393_offline.sh",
            "sha256": "473eb019282c2735d65c6058f6890e60b79a5698ae18d2c1e4489fed8dd18a02",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/19105/l_fortran-compiler_p_2023.0.0.25394_offline.sh",
            "sha256": "fd7525bf90646c8e43721e138f29c9c6f99e96dfe5648c13633f30ec64ac8b1b",
        },
    },
    {
        "version": "2022.2.1",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/19049/l_dpcpp-cpp-compiler_p_2022.2.1.16991_offline.sh",
            "sha256": "3f0f02f9812a0cdf01922d2df9348910c6a4cb4f9dfe50fc7477a59bbb1f7173",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/18998/l_fortran-compiler_p_2022.2.1.16992_offline.sh",
            "sha256": "64f1d1efbcdc3ac2182bec18313ca23f800d94f69758db83a1394490d9d4b042",
        },
    },
    {
        "version": "2022.2.0",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/18849/l_dpcpp-cpp-compiler_p_2022.2.0.8772_offline.sh",
            "sha256": "8ca97f7ea8abf7876df6e10ce2789ea8cbc310c100ad7bf0b5ffccc4f3c7f2c9",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/18909/l_fortran-compiler_p_2022.2.0.8773_offline.sh",
            "sha256": "4054e4bf5146d55638d21612396a19ea623d22cbb8ac63c0a7150773541e0311",
        },
    },
    {
        "version": "2022.1.0",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/18717/l_dpcpp-cpp-compiler_p_2022.1.0.137_offline.sh",
            "sha256": "1027819581ba820470f351abfc2b2658ff2684ed8da9ed0e722a45774a2541d6",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/18703/l_fortran-compiler_p_2022.1.0.134_offline.sh",
            "sha256": "583082abe54a657eb933ea4ba3e988eef892985316be13f3e23e18a3c9515020",
        },
    },
    {
        "version": "2022.0.2",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/18478/l_dpcpp-cpp-compiler_p_2022.0.2.84_offline.sh",
            "sha256": "ade5bbd203e7226ca096d7bf758dce07857252ec54e83908cac3849e6897b8f3",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/18481/l_fortran-compiler_p_2022.0.2.83_offline.sh",
            "sha256": "78532b4118fc3d7afd44e679fc8e7aed1e84efec0d892908d9368e0c7c6b190c",
        },
    },
    {
        "version": "2022.0.1",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/18435/l_dpcpp-cpp-compiler_p_2022.0.1.71_offline.sh",
            "sha256": "c7cddc64c3040eece2dcaf48926ba197bb27e5a46588b1d7b3beddcdc379926a",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/18436/l_fortran-compiler_p_2022.0.1.70_offline.sh",
            "sha256": "2cb28a04f93554bfeffd6cad8bd0e7082735f33d73430655dea86df8933f50d1",
        },
    },
    {
        "version": "2021.4.0",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/18209/l_dpcpp-cpp-compiler_p_2021.4.0.3201_offline.sh",
            "sha256": "9206bff1c2fdeb1ca0d5f79def90dcf3e6c7d5711b9b5adecd96a2ba06503828",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/18210/l_fortran-compiler_p_2021.4.0.3224_offline.sh",
            "sha256": "de2fcf40e296c2e882e1ddf2c45bb8d25aecfbeff2f75fcd7494068d621eb7e0",
        },
    },
    {
        "version": "2021.3.0",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/17928/l_dpcpp-cpp-compiler_p_2021.3.0.3168_offline.sh",
            "sha256": "f848d81b7cabc76c2841c9757abb2290921efd7b82491d830605f5785600e7a1",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/17959/l_fortran-compiler_p_2021.3.0.3168_offline.sh",
            "sha256": "c4553f7e707be8e8e196f625e4e7fbc8eff5474f64ab85fc7146b5ed53ebc87c",
        },
    },
    {
        "version": "2021.2.0",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/17749/l_dpcpp-cpp-compiler_p_2021.2.0.118_offline.sh",
            "sha256": "5d01cbff1a574c3775510cd97ffddd27fdf56d06a6b0c89a826fb23da4336d59",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/17756/l_fortran-compiler_p_2021.2.0.136_offline.sh",
            "sha256": "a62e04a80f6d2f05e67cd5acb03fa58857ee22c6bd581ec0651c0ccd5bdec5a1",
        },
    },
    {
        "version": "2021.1.2",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/17513/l_dpcpp-cpp-compiler_p_2021.1.2.63_offline.sh",
            "sha256": "68d6cb638091990e578e358131c859f3bbbbfbf975c581fd0b4b4d36476d6f0a",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/irc_nas/17508/l_fortran-compiler_p_2021.1.2.62_offline.sh",
            "sha256": "29345145268d08a59fa7eb6e58c7522768466dd98f6d9754540d1a0803596829",
        },
    },
]


@IntelOneApiPackage.update_description
class IntelOneapiCompilers(IntelOneApiPackage):
    """Intel oneAPI Compilers. Includes: icc, icpc, ifort, icx, icpx, ifx,
    and dpcpp.

    """

    maintainers("rscohn2")

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi.html"

    # See https://github.com/spack/spack/issues/39252
    depends_on("patchelf@:0.17", type="build")

    # TODO: effectively gcc is a direct dependency of intel-oneapi-compilers, but we
    # cannot express that properly. For now, add conflicts for non-gcc compilers
    # instead.
    requires("%gcc", msg="intel-oneapi-compilers must be installed with %gcc")

    for v in versions:
        version(v["version"], expand=False, **v["cpp"])
        resource(
            name="fortran-installer",
            placement="fortran-installer",
            when="@{0}".format(v["version"]),
            expand=False,
            **v["ftn"],
        )

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

    def setup_run_environment(self, env):
        """Adds environment variables to the generated module file.

        These environment variables come from running:

        .. code-block:: console

           $ source {prefix}/{component}/{version}/env/vars.sh

        and from setting CC/CXX/F77/FC
        """
        super().setup_run_environment(env)

        env.set("CC", self._llvm_bin.icx)
        env.set("CXX", self._llvm_bin.icpx)
        env.set("F77", self._llvm_bin.ifx)
        env.set("FC", self._llvm_bin.ifx)

    def install(self, spec, prefix):
        # Copy instead of install to speed up debugging
        # install_tree("/opt/intel/oneapi/compiler", self.prefix)
        # return

        # install cpp
        super().install(spec, prefix)

        # install fortran
        self.install_component(find("fortran-installer", "*")[0])

        # Some installers have a bug and do not return an error code when failing
        if not is_exe(self._llvm_bin.ifx):
            raise RuntimeError("Fortran install failed")

    @run_after("install")
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
            p = path.join(compiler + ".cfg")
            with open(p, "w") as f:
                f.write(" ".join(flags))
            set_install_permissions(p)

    @run_after("install")
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
        llvm_flags = ["--gcc-toolchain={}".format(self.compiler.prefix)]
        classic_flags = ["-gcc-name={}".format(self.compiler.cc)]
        classic_flags.append("-gxx-name={}".format(self.compiler.cxx))

        # Older versions trigger -Wunused-command-line-argument warnings whenever
        # linker flags are passed in preprocessor (-E) or compilation mode (-c).
        # The cfg flags are treated as command line flags apparently. Newer versions
        # do not trigger these warnings. In some build systems these warnings can
        # cause feature detection to fail, so we silence them with -Wno-unused-...
        if self.spec.satisfies("@:2022.0"):
            llvm_flags.append("-Wno-unused-command-line-argument")

        self.write_config_file(common_flags + llvm_flags, self._llvm_bin, ["icx", "icpx"])
        self.write_config_file(common_flags + classic_flags, self._llvm_bin, ["ifx"])
        self.write_config_file(common_flags + classic_flags, self._classic_bin, ["ifort"])
        # 2023 is the last release that includes icc
        if self.spec.satisfies("@:2023"):
            self.write_config_file(
                common_flags + classic_flags, self._classic_bin, ["icc", "icpc"]
            )

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
