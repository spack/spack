# Copyright 2022-2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
# https://www.apache.org/licenses/LICENSE-2.0> or the MIT license
# <LICENSE-MIT or https://opensource.org/licenses/MIT>, at your
# option. This file may not be copied, modified, or distributed
# except according to those terms.

import os

from spack.package import *


class Libpsm3(AutotoolsPackage):
    """PSM3 packge for testing new drops from Intel"""

    homepage = "https://ofiwg.github.io/libfabric/v1.12.0/man/fi_psm3.7.html"
    url = "https://github.com/intel/eth-psm3-fi/archive/refs/tags/v11.4.1.0.tar.gz"
    git = "https://github.com/intel/eth-psm3-fi.git"

    # For external sharing?
    # url = "file://{0}/libpsm3-fi-11.4.0.0.tar.bz2".format(os.getcwd())
    # manual_download = True
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
