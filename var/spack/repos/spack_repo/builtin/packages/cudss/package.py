# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *

_versions = {
    "0.5.0": {
        "Linux-x86_64": (
            "5245d2ba26a590839e2f1dd074f87e39ee5cc201c3b29245b35c7060d59c37a5",
            "https://developer.download.nvidia.com/compute/cudss/redist/libcudss/linux-x86_64/libcudss-linux-x86_64-0.5.0.16_cuda12-archive.tar.xz",
        ),
        "Linux-aarch64": (
            "5d07496e90fc0afb334a7e434c86c6083b1e8cf56dc65d70a01bd811e54096d7",
            "https://developer.download.nvidia.com/compute/cudss/redist/libcudss/linux-aarch64/libcudss-linux-aarch64-0.5.0.16_cuda12-archive.tar.xz",
        ),
    }
}


class Cudss(Package):
    """NVIDIA cuDSS is a GPU-accelerated Direct Sparse Solver library
    for solving linear systems with very sparse matrices"""

    homepage = "https://developer.nvidia.com/cudss"

    maintainers("ddement")

    skip_version_audit = ["platform=darwin", "platform=windows"]

    for ver, packages in _versions.items():
        pkg = packages.get(f"{platform.system()}-{platform.machine()}")
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1])

    depends_on("cuda@12:")

    def install(self, spec, prefix):
        install_tree(".", prefix)
