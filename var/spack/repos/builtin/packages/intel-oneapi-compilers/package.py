# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.build_environment import dso_suffix
from spack.package import *

linux_versions = [
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

    maintainers = ["rscohn2"]

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi.html"

    depends_on("patchelf", type="build")

    if platform.system() == "Linux":
        for v in linux_versions:
            version(v["version"], expand=False, **v["cpp"])
            resource(
                name="fortran-installer",
                placement="fortran-installer",
                when="@{0}".format(v["version"]),
                expand=False,
                **v["ftn"]
            )

    @property
    def component_dir(self):
        return "compiler"

    def setup_run_environment(self, env):
        """Adds environment variables to the generated module file.

        These environment variables come from running:

        .. code-block:: console

           $ source {prefix}/{component}/{version}/env/vars.sh

        and from setting CC/CXX/F77/FC
        """
        super(IntelOneapiCompilers, self).setup_run_environment(env)

        env.set("CC", self.component_prefix.bin.icx)
        env.set("CXX", self.component_prefix.bin.icpx)
        env.set("F77", self.component_prefix.bin.ifx)
        env.set("FC", self.component_prefix.bin.ifx)

    def install(self, spec, prefix):
        # Copy instead of install to speed up debugging
        # install_tree('/opt/intel/oneapi/compiler', self.prefix)

        # install cpp
        super(IntelOneapiCompilers, self).install(spec, prefix)

        # install fortran
        self.install_component(find("fortran-installer", "*")[0])

        # Some installers have a bug and do not return an error code when failing
        if not is_exe(self.component_prefix.linux.bin.intel64.ifort):
            raise RuntimeError("install failed")

    @run_after("install")
    def inject_rpaths(self):
        # Sets rpath so the compilers can work without setting LD_LIBRARY_PATH.
        patchelf = which("patchelf")
        patchelf.add_default_arg("--set-rpath")
        patchelf.add_default_arg(":".join(self._ld_library_path()))
        for pd in ["bin", "lib", join_path("compiler", "lib", "intel64_lin")]:
            for file in find(self.component_prefix.linux.join(pd), "*", recursive=False):
                # Try to patch all files, patchelf will do nothing and fail if file
                # should not be patched
                patchelf(file, fail_on_error=False)

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
        flags = " ".join(["-Wl,-rpath,{0}".format(d) for d in self._ld_library_path()])
        for cmp in [
            "icx",
            "icpx",
            "ifx",
            join_path("intel64", "icc"),
            join_path("intel64", "icpc"),
            join_path("intel64", "ifort"),
        ]:
            cfg_file = self.component_prefix.linux.bin.join(cmp + ".cfg")
            with open(cfg_file, "w") as f:
                f.write(flags)
            set_install_permissions(cfg_file)

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
