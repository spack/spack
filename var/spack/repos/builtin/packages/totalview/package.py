# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Totalview(Package):
    """Totalview parallel debugger.

    Select the version associated with your machine architecture'
    '."""

    homepage = "https://totalview.io"
    maintainers("dshrader", "petertea", "suzannepaterno", "elliebinkley")
    license_required = True
    license_comment = "#"
    license_files = ["tv_license/license.lic"]
    license_vars = ["RLM_LICENSE"]

    # As the install of Totalview is via multiple tarballs, the base install
    # will be the documentation.  The architecture-specific tarballs are added
    # as resources dependent on the specific architecture used.

    version(
        "2024.2-x86-64",
        md5="1740fe50dbe87e17b48752e27937838a",
        url="https://dslwuu69twiif.cloudfront.net/totalview/2024.2/totalview_2024.2.11_linux_x86-64.tar",
    )

    version(
       "2024.2-powerle",
        md5="29d0cf1f764ae1fe85caae092e55eb70",
        url="https://dslwuu69twiif.cloudfront.net/totalview/2024.2/totalview_2024.2.11_linux_powerle.tar",
    )

    version(
       "2024.2-linux-arm64",
        md5="91d711f25e3605999fae7ca1290ac949",
        url="https://dslwuu69twiif.cloudfront.net/totalview/2024.2/totalview_2024.2.11_linux_arm64.tar",
    )

    version(
       "2024.1-x86-64",
        md5="c406533efaf7decd23ce569a01bd0ee6",
        url="https://dslwuu69twiif.cloudfront.net/totalview/2024.1/totalview_2024.1.21_linux_x86-64.tar",
    )

    version(
       "2024.1-powerle",
        md5="443736bef3aa7b4ae83bc441ff6acaf6",
        url="https://dslwuu69twiif.cloudfront.net/totalview/2024.1/totalview_2024.1.21_linux_powerle.tar",
    )

    version(
        "2024.1-linux-arm64",
        md5="58dff4cb2a74950d56502016b0676ef7",
        url="https://dslwuu69twiif.cloudfront.net/totalview/2024.1/totalview_2024.1.21_linux_arm64.tar",
    )
    
    def setup_run_environment(self, env):
        env.prepend_path(
            "PATH",
            join_path(self.prefix, "toolworks", "totalview.{0}".format(self.version), "bin"),
        )
        env.prepend_path(
            "TVROOT", join_path(self.prefix, "toolworks", "totalview.{0}".format(self.version))
        )
        env.prepend_path("TVDSVRLAUNCHCMD", "ssh")

    def install(self, spec, prefix):
        # Assemble install line
        install_cmd = which("./Install")
        arg_list = ["-agree", "-nosymlink", "-directory", "{0}".format(prefix)]

        # Platform specification.
        if spec.target.family == "x86_64" and spec.platform == "linux":
            arg_list.extend(["-platform", "linux-x86-64"])
        elif spec.target.family == "aarch64":
            arg_list.extend(["-platform", "linux-arm64"])
        elif spec.target.family == "ppc64le":
            arg_list.extend(["-platform", "linux-powerle"])
        else:
            raise InstallError("Architecture {0} not permitted!".format(spec.target.family))

        install_cmd.exe.extend(arg_list)

        # Run install script for totalview (which automatically installs memoryscape)
        install_cmd = which("./Install")
        arg_list.extend(["-install", "totalview"])
        install_cmd.exe.extend(arg_list)
        install_cmd()

        # If a license file was created
        symlink(
            join_path(self.prefix, "tv_license", "license.lic"),
            join_path(self.prefix, "toolworks", "tv_license", "license.lic"),
        )
