# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class HipRocclr(CMakePackage):
    """Hip-ROCclr is a virtual device interface that compute runtimes interact
    with to different backends such as ROCr or PAL This abstraction allows
    runtimes to work on Windows as well as on Linux without much effort."""

    homepage = "https://github.com/ROCm/ROCclr"
    url = "https://github.com/ROCm/ROCclr/archive/rocm-5.6.1.tar.gz"
    git = "https://github.com/ROCm/ROCclr.git"
    tags = ["rocm"]

    phases = ["cmake", "build"]

    maintainers("srekolam", "renjithravindrankannath")

    license("MIT")

    version("master", branch="main")
    version("5.6.1", sha256="cc9a99c7e4de3d9360c0a471b27d626e84a39c9e60e0aff1e8e1500d82391819")
    version("5.6.0", sha256="864f87323e793e60b16905284fba381a7182b960dd4a37fb67420c174442c03c")
    with default_args(deprecated=True):
        version("5.5.1", sha256="1375fc7723cfaa0ae22a78682186d4804188b0a54990bfd9c0b8eb421b85e37e")
        version("5.5.0", sha256="efbae9a1ef2ab3de5ca44091e9bb78522e76759c43524c1349114f9596cc61d1")
    depends_on("cmake@3:", type="build")
    depends_on("gl@4.5:", type="link")
    depends_on("numactl", type="link")

    for ver in ["5.5.0", "5.5.1", "5.6.0", "5.6.1", "master"]:
        depends_on(f"hsakmt-roct@{ver}", when=f"@{ver}")
        depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")
        depends_on(f"comgr@{ver}", when=f"@{ver}")

    # Add opencl sources thru the below
    for d_version, d_shasum in [
        ("5.6.1", "ec26049f7d93c95050c27ba65472736665ec7a40f25920a868616b2970f6b845"),
        ("5.6.0", "52ab260d00d279c2a86c353901ffd88ee61b934ad89e9eb480f210656705f04e"),
        ("5.5.1", "a8a62a7c6fc5398406d2203b8cb75621a24944688e545d917033d87de2724498"),
        ("5.5.0", "0df9fa0b8aa0c8e6711d34eec0fdf1ed356adcd9625bc8f1ce9b3e72090f3e4f"),
    ]:
        resource(
            name="opencl-on-vdi",
            url=f"https://github.com/ROCm/ROCm-OpenCL-Runtime/archive/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="opencl-on-vdi",
            when=f"@{d_version}",
        )

    resource(
        name="opencl-on-vdi",
        git="https://github.com/ROCm/ROCm-OpenCL-Runtime.git",
        destination="",
        placement="opencl-on-vdi",
        branch="main",
        when="@master",
    )

    def cmake_args(self):
        return [
            self.define("USE_COMGR_LIBRARY", "yes"),
            self.define("OPENCL_DIR", join_path(self.stage.source_path, "opencl-on-vdi")),
        ]
