# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Racon(CMakePackage):
    """Ultrafast consensus module for raw de novo genome assembly of long
    uncorrected reads."""

    homepage = "https://github.com/lbcb-sci/racon"
    url = "https://github.com/lbcb-sci/racon/archive/refs/tags/1.5.0.tar.gz"

    version("1.5.0", sha256="41e362f71cc03b934f17d6e2c0d626e1b2997258261b14551586de006666424a")
    version("1.4.21", sha256="be293cb26d167c5353cacba69f4c86cb6924e234c5e1902e8e4e68ed70217d66")
    version("1.4.20", sha256="50c22e66a1141c865b70917eecf34155b9ab3a4642765381c30f64557bdb2a9f")
    version("1.4.13", sha256="e91e6a7170554230089ebea19b2c2b5134a1677247830d8c5a3b6aa686241387")
    version("1.4.12", sha256="658e04c6f282f53bcc8ffd2c7f97a787b97447d41fef29727eddd96d576efbae")
    version("1.4.11", sha256="f1a45b5a8928ed2e133e6262a0887a99ec19dfba9143cdb8d4747d4530fa699e")
    version("1.4.10", sha256="101c1ba967eda296fea6f88c7ee7b01eb5c912b253dd0b0fdd80399b504808cb")
    version("1.4.9", sha256="ae0bef208271166dd6325440131e408386408c12a9497d8d743504908ecb45e8")
    version("1.4.7", sha256="75e39395ced636dd0f5ef1abe431d8f9f6404eb0a806c530cff8e4fa4f57fab7")
    version("1.4.6", sha256="6514e89e4e6eea1d14fc1b760c4ccd02a833443284259d52628eeea0eb5f70db")

    depends_on("cmake@3.2:", type="build")
    depends_on("python", type="build")
    depends_on("sse2neon", when="target=aarch64:")

    conflicts("%gcc@:4.7")
    conflicts("%clang@:3.1")

    patch('aarch64.patch', when='@:1.4 target=aarch64:')

    def cmake_args(self):
        args = ["-Dracon_build_wrapper=ON"]
        return args
