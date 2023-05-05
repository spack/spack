# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Libpsm3(AutotoolsPackage):
    """PSM3 provider for the PSM3 OFI provider"""

    homepage = "https://ofiwg.github.io/libfabric/v1.12.0/man/fi_psm3.7.html"
    url = "https://github.com/intel/eth-psm3-fi/archive/refs/tags/v11.4.1.0.tar.gz"
    git = "https://github.com/intel/eth-psm3-fi.git"

    version(
        "11.4.1.0",
        sha256="272adb9ec10edf709bfcfccc6b6e9296d25d892c36b845ad577caeb82b70c9ac",
        preferred=True,
    )

    variant("verbs", default=False, description="Enable PSM3 verbs")

    variant("sockets", default=True, description="Enable PSM3 sockets")

    variant("atomics", default=True, description="Enable atomics")

    variant("debug", default=False, description="Enable debugging")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("numactl")
    depends_on("uuid")

    maintainers = ["dodecatheon"]

    def configure_args(self):
        args = []

        args.extend(self.enable_or_disable("debug"))

        if "+verbs" in self.spec:
            args.append("--enable-psm3-verbs")
        else:
            args.append("--disable-psm3-verbs")

        if "+atomics" in self.spec:
            args.append("--enable-atomics")
        else:
            args.append("--disable-atomics")

        if "+sockets" in self.spec:
            args.append("--enable-psm3-sockets")
        else:
            args.append("--disable-psm3-sockets")

        return args

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        install_tree("src/.libs", prefix.lib)
        os.unlink("%s/libpsm3-fi.la" % prefix.lib)
        install("src/libpsm3-fi.la", prefix.lib)

    def setup_run_environment(self, env):
        env.prepend_path("FI_PROVIDER_PATH", self.prefix.lib)
        env.set("FI_PROVIDER", "psm3")
        env.set("PSM3_ALLOW_ROUTERS", "1")
        if "+sockets" in self.spec and "~verbs" in self.spec:
            env.set("PSM3_HAL", "sockets")
        env.set("FI_PSM3_NAME_SERVER", "1")
        if "+debug" in self.spec:
            env.set("PSM3_IDENTIFY", "1")
