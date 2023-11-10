# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SysSage(CMakePackage):
    """A library for capturing hardware topology and attributes of compute systems."""

    homepage = "https://github.com/caps-tum/sys-sage"
    url = "https://github.com/caps-tum/sys-sage/archive/refs/tags/v0.4.3.tar.gz"
    git = "https://github.com/caps-tum/sys-sage.git"

    maintainers = ["stepanvanecek"]

    version("0.4.3", sha256="e24313c4274576c1511a62e1b27c86a78cea7e4c123b8a53303cfc70de978faa")
    version("master", branch="master")
    version("develop", branch="develop")

    conflicts("%gcc@:7", msg="gcc can be used from version 8 and above")

    variant(
        "nvidia_mig",
        default=False,
        description="Build and install functionality regarding NVidia MIG(multi-instance GPU, "
        "ampere or newer).",
    )
    variant(
        "cpuinfo",
        default=True,
        description="Build and install functionality regarding Linux cpuinfo (only x86) -- "
        "default ON.",
    )
    variant(
        "build_data_sources",
        default=False,
        description="Build all data sources (programs to collect data about the machine sys-sage "
        "runs on).",
    )
    variant(
        "ds_hwloc",
        default=False,
        description="Builds the hwloc data source for retrieving the CPU topology",
    )
    variant(
        "ds_numa",
        default=False,
        description="builds the caps-numa-benchmark. If turned on, includes Linux-specific "
        "libraries.",
    )

    depends_on("cmake@3.22:", type="build")
    depends_on("libxml2@2.9.13:")

    depends_on("numactl", when="+build_data_sources platform=linux")
    depends_on("numactl", when="+ds_numa platform=linux")
    depends_on("hwloc@2.9:", when="+build_data_sources")
    depends_on("hwloc@2.9:", when="+ds_hwloc")
    depends_on("cuda", when="+nvidia_mig platform=linux")
    depends_on("cuda", when="+build_data_sources platform=linux")

    def cmake_args(self):
        spec = self.spec
        args = []
        if "+nvidia_mig" in spec:
            args.append("-DNVIDIA_MIG=ON")
        if "+cpuinfo" in spec and spec.target == "x86_64" and spec.platform == "linux":
            args.append("-DCPUINFO=ON")
        else:
            args.append("-DCPUINFO=OFF")
        if "+ds_hwloc" in spec or "+build_data_sources" in spec:
            args.append("-DDS_HWLOC=ON")
        if "+ds_numa" in spec or "+build_data_sources" in spec:
            if spec.platform == "linux":
                args.append("-DDS_NUMA=ON")
            else:
                msg = "ds_numa option is only available on Linux systems."
                raise InvalidSpecDetected(msg)
        return args
