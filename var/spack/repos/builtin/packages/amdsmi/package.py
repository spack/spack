# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Amdsmi(CMakePackage):
    """The AMD System Management Interface Library, or AMD SMI library,
    is a C library for Linux that provides a user space interface for
    applications to monitor and control AMD device."""

    homepage = "https://github.com/RadeonOpenCompute/amdsmi"
    url = "https://github.com/RadeonOpenCompute/amdsmi/archive/refs/tags/rocm-5.6.0.tar.gz"

    tags = ["rocm"]
    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["libamd_smi"]

    version("5.6.0", sha256="595c9d6d79d9071290b2f19ab4ef9222c8d2983b4322b3143fcd9d0b1ce0f6d8")
    version("5.5.1", sha256="b794c7fd562fd92f2c9f2bbdc2d5dded7486101fcd4598f2e8c3484c9a939281")
    version("5.5.0", sha256="dcfbd96e93afcf86b1261464e008e9ef7e521670871a1885e6eaffc7cdc8f555")

    depends_on("cmake@3.11:", type="build")
    depends_on("python@3.6:", type="run")
    depends_on("py-virtualenv", type="build")
    depends_on("llvm@14:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("libdrm", type="build")
    depends_on("py-pyyaml", type="build")

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            ver = "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        else:
            ver = None
        return ver

    def cmake_args(self):
        args = []
        args.append(self.define("BUILD_TESTS", "ON"))
        args.append("-DCMAKE_INSTALL_LIBDIR=lib")
        return args
