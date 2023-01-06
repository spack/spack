# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Squashfuse(AutotoolsPackage):
    """squashfuse - Mount SquashFS archives using FUSE"""

    homepage = "https://github.com/vasi/squashfuse"
    url = "https://github.com/vasi/squashfuse/archive/refs/tags/0.1.105.tar.gz"
    git = "https://github.com/vasi/squashfuse.git"

    maintainers = ["haampie"]

    version("master", branch="master")
    version("0.1.105", sha256="3f776892ab2044ecca417be348e482fee2839db75e35d165b53737cb8153ab1e")
    version("0.1.104", sha256="9e6f4fb65bb3e5de60c8714bb7f5cbb08b5534f7915d6a4aeea008e1c669bd35")
    version("0.1.103", sha256="bba530fe435d8f9195a32c295147677c58b060e2c63d2d4204ed8a6c9621d0dd")
    version("0.1.102", sha256="c2a878b8acceb8e5195af1cf35c869f9dddd6debf24fa9630de1304380108b31")
    version("0.1.101", sha256="4275e1b74ded21de911e73cc3b77bd9f98f2f3c4406030d7f510b6715490a121")
    version("0.1.100", sha256="dda02875735570d24d682cf35846f0165199e0d4ce38e0703e5aabe0318292e6")

    variant("shared", default=True, description="Enable shared libraries")
    variant("static", default=True, description="Enable static libraries")
    variant("min_size", default=False, description="Build small binaries")

    variant("zlib", default=True, description="Enable zlib/gzip compression support")
    variant("lz4", default=True, description="Enable LZ4 compression support")
    variant("lzo", default=True, description="Enable LZO compression support")
    variant("xz", default=True, description="Enable xz compression support")
    variant("zstd", default=True, description="Enable Zstandard/zstd support")

    conflicts("~shared", when="~static", msg="Enable shared, static or both")

    depends_on("fuse@2.5:")
    depends_on("fuse@:2", when="@:0.1.103")

    # Note: typically libfuse is external, but this implies that you have to make
    # pkg-config external too, because spack's pkg-config doesn't know how to
    # locate system pkg-config's fuse.pc/fuse3.pc
    depends_on("pkgconfig", type="build")

    # compression libs
    depends_on("zlib", when="+zlib")
    depends_on("lz4", when="+lz4")
    depends_on("lzo", when="+lzo")
    depends_on("xz", when="+xz")
    depends_on("zstd", when="+zstd")

    depends_on("m4", type="build", when="@master")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    def flag_handler(self, name, flags):
        if name == "cflags" and "+min_size" in self.spec:
            if "-Os" in self.compiler.opt_flags:
                flags.append("-Os")
                return (None, None, flags)

        return (flags, None, None)

    def configure_args(self):
        args = ["--disable-demo"]
        args += self.enable_or_disable("shared")
        args += self.enable_or_disable("static")
        args += self.with_or_without("zlib", activation_value="prefix")
        args += self.with_or_without("lz4", activation_value="prefix")
        args += self.with_or_without("lzo", activation_value="prefix")
        args += self.with_or_without("xz", activation_value="prefix")
        args += self.with_or_without("zstd", activation_value="prefix")
        return args
