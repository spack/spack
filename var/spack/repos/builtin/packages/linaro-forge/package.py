# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import subprocess

from spack.package import *


class LinaroForge(Package):
    """Build reliable and optimized code for the right results on multiple
    Server and HPC architectures, from the latest compilers and C++ standards
    to Intel, 64-bit Arm, AMD, OpenPOWER and Nvidia GPU hardware. Linaro Forge
    combines Linaro DDT, the leading debugger for time-saving high performance
    application debugging, Linaro MAP, the trusted performance profiler for
    invaluable optimization advice across native and Python HPC codes, and
    Linaro Performance Reports for advanced reporting capabilities."""

    homepage = "https://www.linaroforge.com"
    maintainers("kenche-linaro")

    if platform.machine() in ["aarch64", "arm64"]:
        version("23.1", sha256="c9889b95729f97bcffaf0f15b930efbd27081b7cf2ebc958eede3a186cc4d93a")
        version(
            "23.0.4", sha256="a19e6b247badaa52f78815761f71fb95a565024b7f79bdfb2f602f18b47a881c"
        )
        version(
            "23.0.3", sha256="a7e23ef2a187f8e2d6a6692cafb931c9bb614abf58e45ea9c2287191c4c44f02"
        )
        version(
            "23.0.2", sha256="698fda8f7cc05a06909e5dcc50b9956f94135d7b12e84ffb21999a5b45c70c74"
        )
        version(
            "23.0.1", sha256="552e4a3f408ed4eb5f1bfbb83c94530ee8733579c56c3e98050c0ad2d43eb433"
        )
        version("23.0", sha256="7ae20bb27d539751d1776d1e09a65dcce821fc6a75f924675439f791261783fb")
        version(
            "22.1.4", sha256="4e2af481a37b4c99dba0de6fac75ac945316955fc4170d06e321530adea7ac9f"
        )
        version(
            "21.1.3", sha256="4a4ff7372aad5a31fc9e18b7b6c493691ab37d8d44a3158584e62d1ab82b0eeb"
        )
    elif platform.machine() == "ppc64le":
        version("23.1", sha256="39a522c1d9a29f0a35bba5201f3e23c56d87543410505df30c85128816dd455b")
        version(
            "23.0.4", sha256="927c1ba733cf63027243060586b196f8262e545d898712044c359a6af6fc5795"
        )
        version(
            "23.0.3", sha256="5ff9770f4bc4a2df4bac8a2544a9d6bad9fba2556420fa2e659e5c21e741caf7"
        )
        version(
            "23.0.2", sha256="181b157bdfc8609b49addf63023f920ebb609dbc9a126e9dc26605188b756ff0"
        )
        version(
            "23.0.1", sha256="08cffef2195ea96872d56e827f320eed40aaa82fd3b62d4c661a598fb2fb3a47"
        )
        version("23.0", sha256="0962c7e0da0f450cf6daffe1156e1f59e02c9f643df458ec8458527afcde5b4d")
        version(
            "22.1.3", sha256="6479c3a4ae6ce6648c37594eb0266161f06d9f89010fca9299855848661dda49"
        )
        version(
            "22.0.4", sha256="f4cb5bcbaa67f9209299fe4653186a2829760b8b16a2883913aa43766375b04c"
        )
        version(
            "21.1.3", sha256="eecbc5686d60994c5468b2d7cd37bebe5d9ac0ba37bd1f98fbfc69b071db541e"
        )
    elif platform.machine() == "x86_64":
        version("23.1", sha256="31185d5f9855fd03701089907cdf7b38eb72c484ee730f8341decbbd8f9b5930")
        version(
            "23.0.4", sha256="41a81840a273ea9a232efb4f031149867c5eff7a6381d787e18195f1171caac4"
        )
        version(
            "23.0.3", sha256="f2a010b94838f174f057cd89d12d03a89ca946163536eab178dd1ec877cdc27f"
        )
        version(
            "23.0.2", sha256="565f0c073c6c8cbb06c062ca414e3f6ff8c6ca6797b03d247b030a9fbc55a5b1"
        )
        version(
            "23.0.1", sha256="1d681891c0c725363f0f45584c9b79e669d5c9782158453b7d24b4b865d72755"
        )
        version("23.0", sha256="f4ab12289c992dd07cb1a15dd985ef4713d1f9c0cf362ec5e9c995cca9b1cf81")
        version(
            "22.1.3", sha256="4f8a8b1df6ad712e89c82eedf4bd85b93b57b3c8d5b37d13480ff058fa8f4467"
        )
        version(
            "22.0.4", sha256="a2c8c1da38b9684d7c4656a98b3fc42777b03fd474cd0bf969324804f47587e5"
        )
        version(
            "21.1.3", sha256="03dc82f1d075deb6f08d1e3e6592dc9b630d406c08a1316d89c436b5874f3407"
        )

    variant(
        "probe",
        default=False,
        description='Detect available PMU counters via "forge-probe" during install',
    )

    variant("accept-eula", default=False, description="Accept the EULA")

    # forge-probe executes with "/usr/bin/env python"
    depends_on("python@2.7:", type="build", when="+probe")

    # Licensing
    license_required = True
    license_comment = "#"
    license_files = ["licences/Licence"]
    license_vars = [
        "ALLINEA_LICENSE_DIR",
        "ALLINEA_LICENCE_DIR",
        "ALLINEA_LICENSE_FILE",
        "ALLINEA_LICENCE_FILE",
    ]
    license_url = "https://docs.linaroforge.com/latest/html/licenceserver/index.html"

    def url_for_version(self, version):
        pre = "arm" if version < Version("23.0") else "linaro"
        return f"https://downloads.linaroforge.com/{version}/{pre}-forge-{version}-linux-{platform.machine()}.tar"

    @run_before("install")
    def abort_without_eula_acceptance(self):
        install_example = "spack install linaro-forge +accept-eula"
        license_terms_path = os.path.join(self.stage.source_path, "license_terms")
        if not self.spec.variants["accept-eula"].value:
            raise InstallError(
                "\n\n\nNOTE:\nUse +accept-eula "
                + "during installation "
                + "to accept the license terms in:\n"
                + "  {0}\n".format(os.path.join(license_terms_path, "license_agreement.txt"))
                + "  {0}\n\n".format(os.path.join(license_terms_path, "supplementary_terms.txt"))
                + "Example: '{0}'\n".format(install_example)
            )

    def install(self, spec, prefix):
        subprocess.call(["./textinstall.sh", "--accept-license", prefix])
        if spec.satisfies("+probe"):
            probe = join_path(prefix, "bin", "forge-probe")
            subprocess.call([probe, "--install", "global"])

    def setup_run_environment(self, env):
        # Only PATH is needed for Forge.
        # Adding lib to LD_LIBRARY_PATH can cause conflicts with Forge's internal libs.
        env.clear()
        env.prepend_path("PATH", join_path(self.prefix, "bin"))
