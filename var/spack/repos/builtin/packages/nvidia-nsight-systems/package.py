# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import shutil
from glob import glob

from spack.package import *


class NvidiaNsightSystems(Package):
    """NVIDIA Nsight™ Systems is a system-wide performance analysis tool designed
    to visualize an application’s algorithms, identify the largest opportunities
    to optimize, and tune to scale efficiently across any quantity or size of CPUs
    and GPUs, from large servers to the smallest system on a chip"""

    homepage = "https://developer.nvidia.com/nsight-systems"
    url = "https://developer.download.nvidia.com/devtools/repos/"
    maintainers("scothalverson")
    license("NVIDIA Software License Agreement")

    depends_on("libarchive programs='bsdtar'")

    arch = platform.uname()[-1]
    if arch == "x86_64":
        version(
            "2024.1.1",
            sha256="96f57548e0bd69cb02cd1fe8c70ed4a650636ecb3a5ea5ec490c8049adc2beb5",
            url="https://developer.download.nvidia.com/devtools/repos/rhel8/x86_64/nsight-systems-2024.1.1-2024.1.1.59_3380207-0.x86_64.rpm",
            expand=False,
        )
    elif arch == "aarch64":
        version(
            "2024.1.1",
            sha256="41dc15ae128ef1de8e582b66bb465ac6bd67b9d20ef77fc70528b735d80fb3ec",
            url="https://developer.download.nvidia.com/devtools/repos/rhel8/arm64/nsight-systems-2024.1.1-2024.1.1.59_3380207-0.aarch64.rpm",
            expand=False,
        )
    elif arch == "ppc64le":
        version(
            "2024.1.1",
            sha256="8c98b511df1747c4c782430504ae6fa4b3fce6fa72623083a828fc0a1e11f1b8",
            url="https://developer.download.nvidia.com/devtools/repos/rhel8/ppc64le/nsight-systems-cli-2024.1.1-2024.1.1.59_3380207-0.ppc64le.rpm",
            expand=False,
        )

    def install(self, spec, prefix):
        bsdtar = which("bsdtar")
        rpm_file = glob(join_path(self.stage.source_path, "nsight-systems*.rpm"))[0]
        params = ["-x", "-f", rpm_file]
        ver = prefix.split("/")[-1].split("-")[-2]
        bsdtar(*params)

        arch = platform.uname()[-1]
        if arch == "aarch64":
            folders = ["/documentation", "/host-linux-armv8a", "/target-linux-sbsa-armv8"]
        elif arch == "x86_64":
            folders = ["/documentation", "/host-linux-x64", "/target-linux-x64"]
        base_path = ""
        if os.path.exists("opt/nvidia/nsight-systems-cli/"):
            base_path = "opt/nvidia/nsight-systems-cli/"
        elif os.path.exists("opt/nvidia/nsight-systems/"):
            base_path = "opt/nvidia/nsight-systems/"

        for sd in folders:
            shutil.copytree(base_path + ver + sd, prefix + sd)
        os.mkdir(prefix + "/bin")
        os.symlink(prefix + "/host-linux-armv8/nsys-ui", prefix + "/bin/nsys-ui")
        os.symlink(prefix + "/target-linux-sbsa-armv8/nsys", prefix + "/bin/nsys")
