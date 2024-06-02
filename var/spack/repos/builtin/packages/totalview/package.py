# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Totalview(Package):
    """Totalview parallel debugger.

    Source must be made available to Spack
    externally, either by having the tarballs in the current working directory
    or having the tarballs in a Spack mirror.

    The documentation tarball will
    be used as the primary source and the architecture appropriate tarball will
    be downloaded as a resource."""

    homepage = "https://totalview.io"
    maintainers("dshrader", "petertea")
    manual_download = True
    license_required = True
    license_comment = "#"
    license_files = ["licenses/license.dat", "licenses/tv_license_file"]
    license_vars = ["LM_LICENSE_FILE", "TV_LICENSE_FILE"]

    # As the install of Totalview is via multiple tarballs, the base install
    # will be the documentation.  The architecture-specific tarballs are added
    # as resources dependent on the specific architecture used.
    version("2022.3.6", sha256="3f60714b8c885c562433e30c8bcde7e6383b3517664f37f25da7bf7f9110f308")
    version("2022.2.13", sha256="4bf625c760454e532fe66666f2f5479d38f36f569f104bbe3341c0f48cbc8766")
    version("2022.1.11", sha256="0042afdbb024b99350c395decf2606b6913479ab0117bfd7bd4252d91843ef69")
    version("2021.4.10", sha256="c476288ebe1964e0803c7316975c71a957e52f45187b135bc1dc3b65491bb61d")
    version("2021.3.9", sha256="fd947ce755e76a6a06747755aa61bedd0c1428999a46e920db9498ac930ddc29")

    # Distributed with Totalview
    variant("memoryscape", default=True, description="Install memoryscape")

    # Because the actual source tarball is architecture dependent, the main
    # download is the documentation tarball and the source is downloaded as a
    # resource once the target architecture is known.

    # Version 2022.3.6
    resource(
        name="x86-64",
        url="file://totalview.2022.3.6-linux-x86-64.tar",
        destination=".",
        sha256="a2639c52bfd4c7484b728d6a0158239074ff0e0c52208a5452b12b878016a519",
        when="@2022.3.6 platform=linux target=x86_64:",
    )
    resource(
        name="ppcle",
        url="file://totalview_2022.3.6_linux_powerle.tar",
        destination=".",
        sha256="93771a6ce99cff6d11e8172ff57da16aed76ab8ad1804e1d18186fba6de945f7",
        when="@2022.3.6 platform=linux target=ppc64le:",
    )
    resource(
        name="aarch64",
        url="file://totalview_2022.3.6_linux_arm64.tar",
        destination=".",
        sha256="5c18a9a187196980f9bd0fbbb77bb8e5c1d51442188ca44d58a9c49329c98783",
        when="@2022.3.6 platform=linux target=aarch64:",
    )
    resource(
        name="darwinx86",
        url="file://totalview.2022.3.6-darwin-x86.tar",
        destination=".",
        sha256="f558877f7debbeeef200f587edf4cbba41b6bc8db5a0166757445cc652de8a33",
        when="@2022.3.6 platform=darwin target=x86_64:",
    )

    # Version 2022.2.13
    resource(
        name="x86-64",
        url="file://totalview.2022.2.13-linux-x86-64.tar",
        destination=".",
        sha256="aebd11b837ce18b8200859ea762caa56e2cea346daa114f2841aa0f05a422309",
        when="@2022.2.13 platform=linux target=x86_64:",
    )
    resource(
        name="ppcle",
        url="file://totalview_2022.2.13_linux_powerle.tar",
        destination=".",
        sha256="0136be160576b51b03e6409b06d6cc22b5535380894e0fdc6569e2238e12120e",
        when="@2022.2.13 platform=linux target=ppc64le:",
    )
    resource(
        name="aarch64",
        url="file://totalview_2022.2.13_linux_arm64.tar",
        destination=".",
        sha256="d82154222e1ae5fce0bb7abd19b6782494ecb1f76a9a5f38a19e9dcd40bd42aa",
        when="@2022.2.13 platform=linux target=aarch64:",
    )
    resource(
        name="darwinx86",
        url="file://totalview.2022.2.13-darwin-x86.tar",
        destination=".",
        sha256="abcad08e80967959f556cb9f2a7d6dfa7f38e33213fe56f7f3198ff94cd9f3fe",
        when="@2022.2.13 platform=darwin target=x86_64:",
    )

    # Version 2022.1.11
    resource(
        name="x86-64",
        url="file://totalview.2022.1.11-linux-x86-64.tar",
        destination=".",
        sha256="3ec9a7d702572dbbafa41726a036c94b549f9a5911ed6fd6aa55f7b377554bac",
        when="@2022.1.11 platform=linux target=x86_64:",
    )
    resource(
        name="ppcle",
        url="file://totalview_2022.1.11_linux_powerle.tar",
        destination=".",
        sha256="4c49546508f7e0b1a91bea3ea8d71f6f9dc76989c69a4fd78012a4ae8fa44aa6",
        when="@2022.1.11 platform=linux target=ppc64le:",
    )
    resource(
        name="aarch64",
        url="file://totalview_2022.1.11_linux_arm64.tar",
        destination=".",
        sha256="89407c043679d161b6e204fc4ad5686b7ac18742081a045f19388c7294e5ddbe",
        when="@2022.1.11 platform=linux target=aarch64:",
    )
    resource(
        name="darwinx86",
        url="file://totalview.2022.1.11-darwin-x86.tar",
        destination=".",
        sha256="3a99eda8b7be225e0b7596b3c52032809378c86ea736c88e915c0a0e8efedbe4",
        when="@2022.1.11 platform=darwin target=x86_64:",
    )

    # Version 2021.4.10
    resource(
        name="x86-64",
        url="file://totalview.2021.4.10-linux-x86-64.tar",
        destination=".",
        sha256="7e5509b2cfb219100b0032304bdad7d422657c0736c386ba64bdb1bf11d10a1d",
        when="@2021.4.10 platform=linux target=x86_64:",
    )
    resource(
        name="ppcle",
        url="file://totalview_2021.4.10_linux_powerle.tar",
        destination=".",
        sha256="79e812d1cd600172c5ea29c4aa6fb660d293300683419af36dd0e52cd7e15d56",
        when="@2021.4.10 platform=linux target=ppc64le:",
    )
    resource(
        name="aarch64",
        url="file://totalview_2021.4.10_linux_arm64.tar",
        destination=".",
        sha256="46faaae1f33b4f4a20de345611092fbc65cd5759511c1fcf86ca71a0811c76fd",
        when="@2021.4.10 platform=linux target=aarch64:",
    )
    resource(
        name="darwinx86",
        url="file://totalview.2021.4.10-darwin-x86.tar",
        destination=".",
        sha256="adbf95f86763e3cc5ec51fd504f3172bdcbb42a7f1f4e73b17cacca002729ad2",
        when="@2021.4.10 platform=darwin target=x86_64:",
    )

    # Version 2021.3
    resource(
        name="x86_64",
        url="file://totalview_2021.3.9_linux_x86-64.tar",
        destination=".",
        sha256="6315ca855e1bee14678c640c3c9c8207b4f66c91714dcedd4aed592354112b48",
        when="@2021.3.9 platform=linux target=x86_64:",
    )
    resource(
        name="ppcle",
        url="file://totalview_2021.3.9_linux_powerle.tar",
        destination=".",
        sha256="a7657b61895805024f5d4e7550796a485f98ce297a585583cdd20fe0b9b30bbb",
        when="@2021.3.9 platform=linux target=ppc64le:",
    )

    def url_for_version(self, version):
        return "file://{0}/totalview.{1}-doc.tar".format(os.getcwd(), version)

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
        elif spec.target.family == "x86_64" and spec.platform == "darwin":
            arg_list.extend(["-platform", "darwin-x86"])
        elif spec.target.family == "x86":
            arg_list.extend(["-platform", "linux-x86"])
        elif spec.target.family == "aarch64":
            arg_list.extend(["-platform", "linux-arm64"])
        elif spec.target.family == "ppc64le":
            arg_list.extend(["-platform", "linux-powerle"])
        elif spec.target.family == "ppc64":
            arg_list.extend(["-platform", "linux-power"])
        else:
            raise InstallError("Architecture {0} not permitted!".format(spec.target.family))

        # Docs are the "base" install used with every architecture.
        install_cmd.exe.extend(arg_list)
        install_cmd("-install", "doc-pdf")

        # Run install script for totalview (which automatically installs memoryscape)
        with working_dir("./totalview.{0}".format(self.version)):
            install_cmd = which("./Install")
            arg_list.extend(["-install", "totalview"])
            # TotalView automatically installs Memoryscape, so no need to add

            install_cmd.exe.extend(arg_list)
            install_cmd()

        # If a license file was created, link to FNE_license or FNP_license
        symlink(
            join_path(self.prefix, "licenses", "tv_license_file"),
            join_path(self.prefix, "toolworks", "FNE_license", "tv_license_file"),
        )
        symlink(
            join_path(self.prefix, "licenses", "license.dat"),
            join_path(self.prefix, "toolworks", "FNP_license", "license.dat"),
        )
