# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *

ver_pkg_map = {
    "6.0.2": "hsa-amd-aqlprofile_1.0.0.60002.60002-115~20.04_amd64.deb",
    "6.0.0": "hsa-amd-aqlprofile_1.0.0.60000.60000-91~20.04_amd64.deb",
    "5.7.1": "hsa-amd-aqlprofile_1.0.0.50701.50701-98~20.04_amd64.deb",
    "5.7.0": "hsa-amd-aqlprofile_1.0.0.50700.50700-63~20.04_amd64.deb",
    "5.6.1": "hsa-amd-aqlprofile_1.0.0.50601-93~20.04_amd64.deb",
    "5.6.0": "hsa-amd-aqlprofile_1.0.0.50600-67~20.04_amd64.deb",
    "5.5.1": "hsa-amd-aqlprofile_1.0.0.50501-74~20.04_amd64.deb",
    "5.5.0": "hsa-amd-aqlprofile_1.0.0.50500-63~20.04_amd64.deb",
}


class Aqlprofile(Package):
    """
    HSA extension AMD AQL profile library.
    Provides AQL packets helper methods for perfcounters (PMC) and SQ threadtraces (SQTT).
    """

    maintainers("afzpatel", "srekolam", "renjithravindrankannath")

    version(
        ver="6.0.2",
        sha256="57efc4e8380d941fc9e3ba8353bc724913cd5b5be2c53fed016e92da63e31b2f",
        url=f"https://repo.radeon.com/rocm/apt/6.0.2/pool/main/h/hsa-amd-aqlprofile/{ver_pkg_map['6.0.2']}",
        expand=False,
    )
    version(
        ver="6.0.0",
        sha256="e120268933eab5eff25d1b7d0646b0785a13a9fb2dce2bdaca7ac2a19482339c",
        url=f"https://repo.radeon.com/rocm/apt/6.0/pool/main/h/hsa-amd-aqlprofile/{ver_pkg_map['6.0.0']}",
        expand=False,
    )
    version(
        ver="5.7.1",
        sha256="9f00713062005624231dac5fd3e92481b8d1547b3301c3b8a07298d4548037b8",
        url=f"https://repo.radeon.com/rocm/apt/5.7.1/pool/main/h/hsa-amd-aqlprofile/{ver_pkg_map['5.7.1']}",
        expand=False,
    )
    version(
        ver="5.7.0",
        sha256="131e2d699eb24ff19cba54a9721b83c362196c91a8380b5e4b4ba3583311df21",
        url="https://repo.radeon.com/rocm/apt/5.7/pool/main/h/hsa-amd-aqlprofile/{ver_pkg_map['5.7.0']}",
        expand=False,
    )
    version(
        ver="5.6.1",
        sha256="ddb231dc4c8ca45e586ba68cae86273c3bc109f5ec172855815fce1ea6aff172",
        url="https://repo.radeon.com/rocm/apt/5.6.1/pool/main/h/hsa-amd-aqlprofile/{ver_pkg_map['5.6.1']}",
        expand=False,
    )
    version(
        ver="5.6.0",
        sha256="67273e8513c0efdef6d52fb211a0cf4b7e117b1c5e737f8763946699324a9d7d ",
        url="https://repo.radeon.com/rocm/apt/5.6/pool/main/h/hsa-amd-aqlprofile/{ver_pkg_map['5.6.0']}",
        expand=False,
    )
    version(
        ver="5.5.1",
        sha256="67b957abe5ea872abd3ec6b98eb83ef66fe07668001392e695dd77ab1b6d8890",
        url="https://repo.radeon.com/rocm/apt/5.5.1/pool/main/h/hsa-amd-aqlprofile/{ver_pkg_map['5.5.1']}",
        expand=False,
    )
    version(
        ver="5.5.0",
        sha256="fbe08a39a36499959198fa7678338cf2d7888dc2aafb4694072d1f37b24e599f",
        url="https://repo.radeon.com/rocm/apt/5.5/pool/main/h/hsa-amd-aqlprofile/{ver_pkg_map['5.5.0']}",
        expand=False,
    )

    def install(self, spec, prefix):
        # extract lib files from .deb pkg
        deb_pkg_name = ver_pkg_map[str(spec.version)]
        os.system(f"ar vx {deb_pkg_name}")
        os.system("tar xvf data.tar.gz")

        install_tree(f"opt/rocm-{spec.version}/share/", prefix.share)
        install_tree(f"opt/rocm-{spec.version}/lib/", prefix.lib)
