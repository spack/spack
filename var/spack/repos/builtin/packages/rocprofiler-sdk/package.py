# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.platforms
from spack.package import *

_versions = {
    "6.3.2": {
        "apt": (
            "28310272952cde3462c856cbf130c5b4bbe0231f51b9ddc0993e4500d8f00abb",
            "https://repo.radeon.com/rocm/apt/6.3.2/pool/main/r/rocprofiler-sdk/rocprofiler-sdk_0.5.0-66~20.04_amd64.deb",
        ),
        "yum": (
            "bc51c3d7e187db485a09cd26373e45189ff20661ec66825a9340329c9c7361ba",
            "https://repo.radeon.com/rocm/rhel8/6.3.2/main/rocprofiler-sdk-0.5.0.60302-66.el8.x86_64.rpm",
        ),
        "zyp": (
            "279fd6d925d6abeb22a0b41d70a015a10d75521570a556199f12ae2c954a20d6",
            "https://repo.radeon.com/rocm/zyp/6.3.2/main/rocprofiler-sdk-0.5.0.60302-sles155.66.x86_64.rpm",
        ),
    },
    "6.3.1": {
        "apt": (
            "fa79a3611fa1502bd21f7cb380da9e5be3d00ec35696b2b3a19b502ccbc7afb8",
            "https://repo.radeon.com/rocm/apt/6.3.1/pool/main/r/rocprofiler-sdk/rocprofiler-sdk_0.5.0-48~20.04_amd64.deb",
        ),
        "yum": (
            "5075fdc0fbec83a386c125961df2873621d4d3acc93dc330b1b1fd48e4d2ab5a",
            "https://repo.radeon.com/rocm/rhel8/6.3.1/main/rocprofiler-sdk-0.5.0.60301-48.el8.x86_64.rpm",
        ),
        "zyp": (
            "633a46d7b6d6c8b27fdff0cd2de05c15724cd014696b99794b51d5439cd73bc9",
            "https://repo.radeon.com/rocm/zyp/6.3.1/main/rocprofiler-sdk-0.5.0.60301-sles155.48.x86_64.rpm",
        ),
    },
    "6.3.0": {
        "apt": (
            "a023617ad37362b9d5453f9fa3b56c32854fa85363376367648211b17a5f9a48",
            "https://repo.radeon.com/rocm/apt/6.3/pool/main/r/rocprofiler-sdk/rocprofiler-sdk_0.5.0-39~20.04_amd64.deb",
        ),
        "yum": (
            "2497ff0f73deda125c9b37ad9ee676faa7dfe261df4cbcdd260a8a613bd51536",
            "https://repo.radeon.com/rocm/rhel8/6.3/main/rocprofiler-sdk-0.5.0.60300-39.el8.x86_64.rpm",
        ),
        "zyp": (
            "396d17a5b4ef0fca782f6a78561bd58e1eb585516d4b75ef2017f5b78d680a85",
            "https://repo.radeon.com/rocm/zyp/6.3/main/rocprofiler-sdk-0.5.0.60300-sles155.39.x86_64.rpm",
        ),
    },
    "6.2.4": {
        "apt": (
            "229ee90e8828e32707cc8abc3c34e6257b6f345d114b680b05459d7eaffb2143",
            "https://repo.radeon.com/rocm/apt/6.2.4/pool/main/r/rocprofiler-sdk/rocprofiler-sdk_0.4.0-139~20.04_amd64.deb",
        ),
        "yum": (
            "92313a469a33f482e973b66f54c8ed904c0f4a71db59abd28459eb58cdc31ffe",
            "https://repo.radeon.com/rocm/rhel8/6.2.4/main/rocprofiler-sdk-0.4.0-139.el8.x86_64.rpm",
        ),
        "zyp": (
            "df015bf40a154cba13c4cea43bcb9940ed5f9e1debaafa1d431f9dd090770cdc",
            "https://repo.radeon.com/rocm/zyp/6.2.4/main/rocprofiler-sdk-0.4.0-sles155.139.x86_64.rpm",
        ),
    },
}


class RocprofilerSdk(Package):
    """
    ROCProfiler-SDK is AMD’s new and improved tooling infrastructure, providing a
    hardware-specific low-level performance analysis interface for profiling and
    tracing GPU compute applications.
    """

    maintainers("afzpatel", "srekolam", "renjithravindrankannath")

    spack_os = spack.platforms.host().default_os
    if "rhel" in spack_os or "centos" in spack_os:
        pkg_type = "yum"
    elif "sles" in spack_os:
        pkg_type = "zyp"
    else:
        pkg_type = "apt"

    for ver, packages in _versions.items():
        pkg = packages.get(pkg_type)
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1], expand=False)

    depends_on("cpio")

    for ver in ["6.2.4", "6.3.0", "6.3.1", "6.3.2"]:
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"rocm-cmake@{ver}", type="build", when=f"@{ver}")

    def install(self, spec, prefix):
        # find deb or rpm pkg and extract files
        for file in os.listdir("."):
            if file.endswith(".rpm"):
                os.system(f"rpm2cpio {file} | cpio -idmv")
                break
            if file.endswith(".deb"):
                os.system(f"ar vx {file}")
                os.system("tar xvf data.tar.gz")
                break

        install_tree(f"opt/rocm-{spec.version}/lib/", prefix.lib)
        install_tree(f"opt/rocm-{spec.version}/share/", prefix.share)
        install_tree(f"opt/rocm-{spec.version}/bin/", prefix.bin)
        install_tree(f"opt/rocm-{spec.version}/libexec/", prefix.libexec)
        install_tree(f"opt/rocm-{spec.version}/include/", prefix.include)

    # This package is installed from binaries, and we haven't patched rpaths.
    unresolved_libraries = ["*"]
