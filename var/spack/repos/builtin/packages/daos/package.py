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
    variant(
        "debug", default=False, description="Enable debugging info and strict compile warnings"
    )

    depends_on("argobots")
    depends_on("boost@develop+python", type="build")
    depends_on("cmocka", type="build")
    depends_on("dpdk@22.11:")
    depends_on("go", type="build")
    depends_on("hwloc")
    depends_on("isa-l")
    depends_on("isa-l_crypto")
    depends_on("libfabric")
    depends_on("libfuse@3.6.1:")
    depends_on("libuuid")
    depends_on("libunwind")
    depends_on("libyaml")
    depends_on("mercury+boostsys")
    depends_on("mpich")
    depends_on("openssl")
    depends_on("pmdk")
    depends_on("protobuf-c")
    depends_on("py-distro")
    depends_on("readline")
    depends_on("scons@4.4.0:")
    depends_on("spdk@23.01:+shared+rdma")

    def build_args(self, spec, prefix):
        args = ["PREFIX={0}".format(prefix), "--build-deps=yes"]

        if "+debug" in spec:
            args.append("--debug=explain,findlibs,includes")

        # Construct ALT_PREFIX and make sure that '/usr' is last.
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
        return args

    def install_args(self, spec, prefix):
        args = ["PREFIX={0}".format(prefix)]
        return args
