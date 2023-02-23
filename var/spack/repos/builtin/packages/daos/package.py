# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Daos(SConsPackage):
    """The Distributed Asynchronous Object Storage (DAOS) is an open-source
    software-defined object store designed from the ground up for massively
    distributed Non Volatile Memory (NVM)."""

    homepage = "https://github.com/daos-stack/daos"
    git = "https://github.com/daos-stack/daos.git"
    maintainers("hyoklee")

    version("master", branch="master", submodules=True)
    version("2.2.0", tag="v2.2.0", submodules=True)
    version("2.0.2", tag="v2.0.2", submodules=True)
    version("1.2.0", tag="v1.2.0", submodules=True)
    version("1.1.4", tag="v1.1.4", submodules=True)
    version("1.1.3", tag="v1.1.3", submodules=True)
    version("1.1.2.1", tag="v1.1.2.1", submodules=True)
    version("1.1.2", tag="v1.1.2", submodules=True)
    version("1.1.1", tag="v1.1.1", submodules=True)
    version("1.0.0", tag="v1.0.0", submodules=True)
    version("0.9.0", tag="v0.9.0", submodules=True)
    version("0.8.0", tag="v0.8.0", submodules=True)
    version("0.7.0", tag="v0.7.0", submodules=True)
    version("0.6.0", tag="v0.6", submodules=True)

    variant("fwd", default=True, description="Bypass root setup and privilege helper")
    variant(
        "debug", default=False, description="Enable debugging info and strict compile warnings"
    )

    depends_on("argobots")
    depends_on("boost@develop+python", type="build", when="@1.1.0:")
    depends_on("cart@daos-1.0", when="@1.0.0")
    depends_on("cart@daos-0.9", when="@0.9.0")
    depends_on("cart@daos-0.8", when="@0.8.0")
    depends_on("cart@daos-0.7", when="@0.7.0")
    depends_on("cart@daos-0.6", when="@0.6.0")
    depends_on("cmocka", type="build")
    depends_on("dpdk@main")
    depends_on("libfuse@3.6.1:")
    depends_on("hwloc@master")
    depends_on("go", type="build")
    depends_on("isa-l")
    depends_on("isa-l-crypto", when="@1.1.0:")
    depends_on("libfabric", when="@0.7.0:")
    depends_on("libuuid")
    depends_on("libunwind")
    depends_on("libyaml")
    depends_on("mercury+boostsys", when="@1.1.0:")
    depends_on("mpich")
    depends_on("openssl")
    depends_on("pmdk")
    depends_on("pmdk@1.11.1:", when="@2.0.0:")
    depends_on("protobuf-c")
    depends_on("py-distro")
    depends_on("readline")
    depends_on("scons@4.4.0")
    depends_on("spdk+shared+rdma")
    depends_on("spdk@18.07.1+fio", when="@0.6.0")
    depends_on("spdk@19.04.1+shared", when="@0.7.0:1.0.0")
    depends_on("spdk@20.01+shared+rdma", when="@1.1.0:1.2.0")

    patch("daos_goreq_1_0.patch", when="@1.0.0")
    patch("daos_goreq_0_8.patch", when="@0.8.0:0.9.0")
    patch("daos_goreq_0_7.patch", when="@0.7.0")
    patch("daos_goreq_0_6.patch", when="@0.6.0")
    patch("daos_werror_scons.patch", when="@:0.9.0")
    patch("daos_disable_python.patch", when="@0.7.0:1.0.0")
    patch("daos_admin_0_9.patch", when="@0.9.0+fwd")
    patch("daos_admin_1_0.patch", when="@1.0.0+fwd")
    patch("daos_load_mpi_0_9.patch", when="@0.9.0:1.0.0")
    patch("daos_dfs.patch", when="@0.9.0:1.0.0")
    patch("daos_extern.patch", when="@0.9.0:1.0.0")
    patch("daos_allow_fwd_1_1_1.patch", when="@1.1.1+fwd")
    patch("daos_load_mpi_1_1_1.patch", when="@1.1.1")
    patch("daos_load_mpi_1_1_2.patch", when="@1.1.2")
    patch("daos_allow_fwd_1_1_2.patch", when="@1.1.2:1.2.0+fwd")
    patch("daos_load_mpi_1_1_3.patch", when="@1.1.3:1.2.0")
    patch("daos_dpdk.patch", when="@2.0.0:2.0.2")
    patch("daos_allow_fwd_2_0_0.patch", when="@2.0.0:2.0.2")

    def build_args(self, spec, prefix):
        args = [
            "PREFIX={0}".format(prefix),
            "--build-deps=yes",
            "--debug=explain,findlibs,includes",
        ]

        if self.spec.satisfies("@1.0.0"):
            args.append("--warning-level=warning")

        if self.spec.satisfies("@:1.0.0"):
            args.extend(
                [
                    "ARGOBOTS_PREBUILT={0}".format(spec["argobots"].prefix),
                    "CART_PREBUILT={0}".format(spec["cart"].prefix),
                    "CMOCKA_PREBUILT={0}".format(spec["cmocka"].prefix),
                    "CRYPTO_PREBUILT={0}".format(spec["openssl"].prefix),
                    "FUSE_PREBUILT={0}".format(spec["libfuse"].prefix),
                    "GO_PREBUILT={0}".format(spec["go"].prefix),
                    "HWLOC_PREBUILT={0}".format(spec["hwloc"].prefix),
                    "ISAL_PREBUILT={0}".format(spec["isa-l"].prefix),
                    "PMDK_PREBUILT={0}".format(spec["pmdk"].prefix),
                    "PROTOBUFC_PREBUILT={0}".format(spec["protobuf-c"].prefix),
                    "SPDK_PREBUILT={0}".format(spec["spdk"].prefix),
                    "UUID_PREBUILT={0}".format(spec["libuuid"].prefix),
                    "YAML_PREBUILT={0}".format(spec["libyaml"].prefix),
                ]
            )

        if self.spec.satisfies("@1.1.0:"):
            # Construct ALT_PREFIX and make sure '/usr' is last
            alt_prefix = [
                format(spec["argobots"].prefix),
                format(spec["boost"].prefix),
                format(spec["cmocka"].prefix),
                format(spec["dpdk"].prefix),
                format(spec["libfabric"].prefix),
                format(spec["libfuse"].prefix),
                format(spec["libuuid"].prefix),
                format(spec["libyaml"].prefix),
                format(spec["hwloc"].prefix),
                format(spec["isa-l"].prefix),
                format(spec["isa-l_crypto"].prefix),
                format(spec["mercury"].prefix),
                format(spec["meson"].prefix),
                format(spec["openssl"].prefix),
                format(spec["pmdk"].prefix),
                format(spec["protobuf-c"].prefix),
                format(spec["spdk"].prefix),
            ]
            alt_prefix_clean = []
            for i in alt_prefix:
                if i != "/usr":
                    alt_prefix_clean.append(i)
            alt_prefix_clean.append("/usr")

            args.extend(
                [
                    "WARNING_LEVEL=warning",
                    "ALT_PREFIX=%s" % ":".join([str(elem) for elem in alt_prefix_clean]),
                    "GO_BIN={0}".format(spec["go"].prefix.bin) + "/go",
                ]
            )

        if self.spec.satisfies("@:0.8.0"):
            args.append("OMPI_PREBUILT={0}".format(spec["openmpi"].prefix))

        if self.spec.satisfies("@0.7.0:1.0.0"):
            args.append("OFI_PREBUILT={0}".format(spec["libfabric"].prefix))

        return args

    def install_args(self, spec, prefix):
        args = ["PREFIX={0}".format(prefix)]

        if self.spec.satisfies("@1.0.0"):
            args.append("--warning-level=warning")

        if self.spec.satisfies("@1.0.0"):
            args.append("WARNING_LEVEL=warning")

        return args
