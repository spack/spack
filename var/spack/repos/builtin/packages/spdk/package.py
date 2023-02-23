# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Spdk(AutotoolsPackage):
    """The Storage Performance Development Kit (SPDK) provides a set of tools
    and libraries for writing high performance, scalable, user-mode storage
    applications. It achieves high performance by moving all of the
    necessary drivers into userspace and operating in a polled mode instead
    of relying on interrupts, which avoids kernel context switches and
    eliminates interrupt handling overhead.
    """

    homepage = "https://spdk.io"
    url = "https://github.com/spdk/spdk/archive/v23.01.tar.gz"
    git = "https://github.com/spdk/spdk"
    maintainers("hyoklee")

    version("master", branch="master", submodules=True)
    version("23.01", tag="v23.01", submodules=True)
    version("22.01.2", tag="v22.01.2", submodules=True)
    version("21.07", tag="v21.07", submodules=True)
    version("20.01.2", tag="v20.01.2", submodules=True)
    version("20.01.1", tag="v20.01.1", submodules=True)
    version("19.04.1", tag="v19.04.1", submodules=True)
    version("19.04", tag="v19.04", submodules=True)
    version("19.01.1", tag="v19.01.1", submodules=True)
    version("19.01", tag="v19.01", submodules=True)
    version("18.10.2", tag="v18.10.2", submodules=True)
    version("18.10.1", tag="v18.10.1", submodules=True)
    version("18.10", tag="v18.10", submodules=True)
    version("18.07.1", tag="v18.07.1", submodules=True)
    version("18.07", tag="v18.07", submodules=True)

    variant("crypto", default=False, description="Build vbdev crypto module")
    variant("fio", default=False, description="Build fio plugin")
    variant("vhost", default=False, description="Build vhost target")
    variant(
        "virtio", default=False, description="Build vhost initiator and virtio-pci bdev modules"
    )
    variant("pmdk", default=False, description="Build persistent memory bdev")
    variant(
        "reduce",
        when="@18.07:22.01.2",
        default=False,
        description="Build vbdev compression module",
    )
    variant("rbd", default=False, description="Build Ceph RBD bdev module")
    variant(
        "rdma", default=False, description="Build RDMA transport for NVMf target and initiator"
    )
    variant("shared", default=False, description="Build spdk shared libraries")
    variant("iscsi-initiator", default=False, description="Build with iscsi bdev module")
    variant(
        "vtune",
        default=False,
        description="Required to profile I/O under Intel VTune Amplifier XE",
    )
    variant("ocf", default=False, description="Build OCF library and bdev module")
    variant("isal", when="@18.07:22.01.2", default=False, description="Build with ISA-L")
    variant("uring", default=False, description="Build I/O uring bdev")

    mods = (
        "crypto",
        "vhost",
        "virtio",
        "pmdk",
        "rbd",
        "rdma",
        "shared",
        "iscsi-initiator",
        "vtune",
        "ocf",
        "uring",
    )

    depends_on("dpdk@main")
    depends_on("nasm@2.12.02:", type="build")
    depends_on("fio@3.3", when="+fio")
    depends_on("meson")
    depends_on("numactl")
    depends_on("libaio")
    depends_on("py-pyelftools")
    depends_on("rdma-core", when="+rdma")

    def configure_args(self):
        spec = self.spec
        config_args = ["--disable-tests"]

        if spec.satisfies("@18.07:22.01.2"):
            self.mods = self.mods + ("reduce", "isal")

        if spec.satisfies("@21.07:"):
            config_args.append("--disable-unit-tests")
            config_args.append("--disable-apps")

        if "+fio" in spec:
            config_args.append("--with-fio={0}".format(spec["fio"].prefix))

        for mod in self.mods:
            if "+" + mod in spec:
                config_args.append("--with-{0}".format(mod))
            else:
                config_args.append("--without-{0}".format(mod))

        return config_args

    @run_after("install")
    def install_additional_files(self):
        spec = self.spec
        prefix = self.prefix

        if spec.satisfies("@19.04:20.01"):
            for file in os.listdir(join_path(self.stage.source_path, "dpdk", "build", "lib")):
                install(join_path("dpdk", "build", "lib", file), prefix.lib)

        if spec.satisfies("@21.07:"):
            dpdk_build_dir = join_path(self.stage.source_path, "dpdk", "build", "lib")
            install_tree(
                join_path(dpdk_build_dir, "pkgconfig"), join_path(prefix.lib, "pkgconfig")
            )
            for file in os.listdir(dpdk_build_dir):
                if os.path.isfile(join_path("dpdk", "build", "lib", file)):
                    install(join_path("dpdk", "build", "lib", file), prefix.lib)
            mkdir(join_path(prefix.include, "dpdk"))
            install_tree("dpdk/build/include", join_path(prefix.include, "dpdk"))

        # Copy the config.h file, as some packages might require it
        mkdir(prefix.share)
        mkdir(join_path(prefix.share, "spdk"))
        install_tree("examples/nvme/fio_plugin", join_path(prefix.share, "spdk", "fio_plugin"))
        install_tree("include", join_path(prefix.share, "spdk", "include"))
        install_tree("scripts", join_path(prefix.share, "spdk", "scripts"))
