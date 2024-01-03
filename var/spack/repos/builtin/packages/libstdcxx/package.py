# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import glob
import itertools
import os
import re
import sys

from archspec.cpu import UnsupportedMicroarchitecture

import llnl.util.filesystem as fs
import llnl.util.tty as tty
from llnl.util.lang import classproperty
from llnl.util.link_tree import LinkTree

import spack.platforms
import spack.util.executable
from spack.build_environment import dso_suffix
from spack.operating_systems.mac_os import macos_sdk_path, macos_version
from spack.package import *


class Libstdcxx(AutotoolsPackage, GNUMirrorPackage):
    """The GNU C++ standard library."""

    homepage = "https://gcc.gnu.org"
    gnu_mirror_path = "gcc/gcc-9.2.0/gcc-9.2.0.tar.xz"
    git = "git://gcc.gnu.org/git/gcc.git"
    list_url = "https://ftp.gnu.org/gnu/gcc/"
    list_depth = 1
    keep_werror = "all"

    maintainers("michaelkuhn", "alalazo")

    version("master", branch="master")

    version("13.2.0", sha256="e275e76442a6067341a27f04c5c6b83d8613144004c0413528863dc6b5c743da")
    version("13.1.0", sha256="61d684f0aa5e76ac6585ad8898a2427aade8979ed5e7f85492286c4dfc13ee86")

    version("12.3.0", sha256="949a5d4f99e786421a93b532b22ffab5578de7321369975b91aec97adfda8c3b")
    version("12.2.0", sha256="e549cf9cf3594a00e27b6589d4322d70e0720cdd213f39beb4181e06926230ff")
    version("12.1.0", sha256="62fd634889f31c02b64af2c468f064b47ad1ca78411c45abe6ac4b5f8dd19c7b")

    version("11.4.0", sha256="3f2db222b007e8a4a23cd5ba56726ef08e8b1f1eb2055ee72c1402cea73a8dd9")
    version("11.3.0", sha256="b47cf2818691f5b1e21df2bb38c795fac2cfbd640ede2d0a5e1c89e338a3ac39")
    version("11.2.0", sha256="d08edc536b54c372a1010ff6619dd274c0f1603aa49212ba20f7aa2cda36fa8b")
    version("11.1.0", sha256="4c4a6fb8a8396059241c2e674b85b351c26a5d678274007f076957afa1cc9ddf")

    version("10.5.0", sha256="25109543fdf46f397c347b5d8b7a2c7e5694a5a51cce4b9c6e1ea8a71ca307c1")
    version("10.4.0", sha256="c9297d5bcd7cb43f3dfc2fed5389e948c9312fd962ef6a4ce455cff963ebe4f1")
    version("10.3.0", sha256="64f404c1a650f27fc33da242e1f2df54952e3963a49e06e73f6940f3223ac344")
    version("10.2.0", sha256="b8dd4368bb9c7f0b98188317ee0254dd8cc99d1e3a18d0ff146c855fe16c1d8c")
    version("10.1.0", sha256="b6898a23844b656f1b68691c5c012036c2e694ac4b53a8918d4712ad876e7ea2")

    version("9.5.0", sha256="27769f64ef1d4cd5e2be8682c0c93f9887983e6cfd1a927ce5a0a2915a95cf8f")
    version("9.4.0", sha256="c95da32f440378d7751dd95533186f7fc05ceb4fb65eb5b85234e6299eb9838e")
    version("9.3.0", sha256="71e197867611f6054aa1119b13a0c0abac12834765fe2d81f35ac57f84f742d1")
    version("9.2.0", sha256="ea6ef08f121239da5695f76c9b33637a118dcf63e24164422231917fa61fb206")
    version("9.1.0", sha256="79a66834e96a6050d8fe78db2c3b32fb285b230b855d0a66288235bc04b327a0")

    version("8.5.0", sha256="d308841a511bb830a6100397b0042db24ce11f642dab6ea6ee44842e5325ed50")
    version("8.4.0", sha256="e30a6e52d10e1f27ed55104ad233c30bd1e99cfb5ff98ab022dc941edd1b2dd4")
    version("8.3.0", sha256="64baadfe6cc0f4947a84cb12d7f0dfaf45bb58b7e92461639596c21e02d97d2c")
    version("8.2.0", sha256="196c3c04ba2613f893283977e6011b2345d1cd1af9abeac58e916b1aab3e0080")
    version("8.1.0", sha256="1d1866f992626e61349a1ccd0b8d5253816222cdc13390dcfaa74b093aa2b153")

    version("7.5.0", sha256="b81946e7f01f90528a1f7352ab08cc602b9ccc05d4e44da4bd501c5a189ee661")
    version("7.4.0", sha256="eddde28d04f334aec1604456e536416549e9b1aa137fc69204e65eb0c009fe51")
    version("7.3.0", sha256="832ca6ae04636adbb430e865a1451adf6979ab44ca1c8374f61fba65645ce15c")
    version("7.2.0", sha256="1cf7adf8ff4b5aa49041c8734bbcf1ad18cc4c94d0029aae0f4e48841088479a")
    version("7.1.0", sha256="8a8136c235f64c6fef69cac0d73a46a1a09bb250776a050aec8f9fc880bebc17")

    version("6.5.0", sha256="7ef1796ce497e89479183702635b14bb7a46b53249209a5e0f999bebf4740945")
    version("6.4.0", sha256="850bf21eafdfe5cd5f6827148184c08c4a0852a37ccf36ce69855334d2c914d4")
    version("6.3.0", sha256="f06ae7f3f790fbf0f018f6d40e844451e6bc3b7bc96e128e63b09825c1f8b29f")
    version("6.2.0", sha256="9944589fc722d3e66308c0ce5257788ebd7872982a718aa2516123940671b7c5")
    version("6.1.0", sha256="09c4c85cabebb971b1de732a0219609f93fc0af5f86f6e437fd8d7f832f1a351")

    version("5.5.0", sha256="530cea139d82fe542b358961130c69cfde8b3d14556370b65823d2f91f0ced87")
    version("5.4.0", sha256="608df76dec2d34de6558249d8af4cbee21eceddbcb580d666f7a5a583ca3303a")
    version("5.3.0", sha256="b84f5592e9218b73dbae612b5253035a7b34a9a1f7688d2e1bfaaf7267d5c4db")
    version("5.2.0", sha256="5f835b04b5f7dd4f4d2dc96190ec1621b8d89f2dc6f638f9f8bc1b1014ba8cad")
    version("5.1.0", sha256="b7dafdf89cbb0e20333dbf5b5349319ae06e3d1a30bf3515b5488f7e89dca5ad")

    version("4.9.4", sha256="6c11d292cd01b294f9f84c9a59c230d80e9e4a47e5c6355f046bb36d4f358092")
    version("4.9.3", sha256="2332b2a5a321b57508b9031354a8503af6fdfb868b8c1748d33028d100a8b67e")
    version("4.9.2", sha256="2020c98295856aa13fda0f2f3a4794490757fc24bcca918d52cc8b4917b972dd")
    version("4.9.1", sha256="d334781a124ada6f38e63b545e2a3b8c2183049515a1abab6d513f109f1d717e")
    version("4.8.5", sha256="22fb1e7e0f68a63cee631d85b20461d1ea6bda162f03096350e38c8d427ecf23")
    version("4.8.4", sha256="4a80aa23798b8e9b5793494b8c976b39b8d9aa2e53cd5ed5534aff662a7f8695")
    version("4.7.4", sha256="92e61c6dc3a0a449e62d72a38185fda550168a86702dea07125ebd3ec3996282")
    version("4.6.4", sha256="35af16afa0b67af9b8eb15cafb76d2bc5f568540552522f5dc2c88dd45d977e8")
    version("4.5.4", sha256="eef3f0456db8c3d992cbb51d5d32558190bc14f3bc19383dd93acc27acc6befc")

    variant("binutils", default=False, description="Build via binutils")
    variant(
        "build_type",
        default="RelWithDebInfo",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
        description="CMake-like build type. "
        "Debug: -O0 -g; Release: -O3; "
        "RelWithDebInfo: -O2 -g; MinSizeRel: -Os",
    )
    variant(
        "stage1",
        default=False,
        description="build a spack sysroot bootstrap compiler, value is the sysroot view path DO NOT USE unless you know what this means",
    )

    depends_on("glibc")

    # mawk is not sufficient for go support
    depends_on("gawk@3.1.5:", type="build")
    depends_on("texinfo@4.7:", type="build")
    depends_on("libtool", type="build")
    # dependencies required for git versions
    depends_on("m4@1.4.6:", type="build")
    depends_on("automake@1.15.1:", type="build")
    # gcc's autoconf checks for *exactly* 2.69
    depends_on("autoconf@2.69", type="build")

    depends_on("gmake@3.80:", type="build")
    depends_on("perl@5", type="build")

    depends_on(
        "binutils+gas+ld+plugins~libiberty", when="+binutils", type=("build", "link", "run")
    )

    # The server is sometimes a bit slow to respond
    timeout = {"timeout": 60}

    # TODO: integrate these libraries.
    # depends_on('ppl')
    # depends_on('cloog')

    # For a list of valid languages for a specific release,
    # run the following command in the GCC source directory:
    #    $ grep ^language= gcc/*/config-lang.in
    # See https://gcc.gnu.org/install/configure.html

    # Binutils can't build ld on macOS
    conflicts("+binutils", when="platform=darwin")

    # aarch64/M1 is supported in GCC 11.3-12.2 and 13
    requires(
        "@11.3,12.2,13.1:",
        when="target=aarch64: platform=darwin",
        msg="Only GCC 11.3-12.2, 13.1+ support macOS M1 (aarch64)",
    )

    # Newer binutils than RHEL's is required to run `as` on some instructions
    # generated by new GCC (see https://github.com/spack/spack/issues/12235)
    conflicts("~binutils", when="@7: os=rhel6", msg="New GCC cannot use system assembler on RHEL6")
    # Ditto for RHEL7/8: OpenBLAS uses flags which the RHEL system-binutils don't have:
    # https://github.com/xianyi/OpenBLAS/issues/3805#issuecomment-1319878852
    conflicts(
        "~binutils", when="@10: os=rhel7", msg="gcc: Add +binutils - preinstalled as might be old"
    )
    conflicts(
        "~binutils", when="@10: os=rhel8", msg="gcc: Add +binutils - preinstalled as might be old"
    )

    # GCC 11 requires GCC 4.8 or later (https://gcc.gnu.org/gcc-11/changes.html)
    conflicts("%gcc@:4.7", when="@11:")

    # https://github.com/iains/gcc-12-branch/issues/6
    conflicts("@:12", when="%apple-clang@14:14.0")

    build_directory = "spack-build"

    def url_for_version(self, version):
        # This function will be called when trying to fetch from url, before
        # mirrors are tried. It takes care of modifying the suffix of gnu
        # mirror path so that Spack will also look for the correct file in
        # the mirrors
        if (version < Version("6.4.0") and version != Version("5.5.0")) or version == Version(
            "7.1.0"
        ):
            self.gnu_mirror_path = self.gnu_mirror_path.replace("xz", "bz2")
        return super().url_for_version(version)

    def configure(self, pkg, spec):
        """Run "configure", with the arguments specified by the builder and an
        appropriately set prefix.
        """
        options = []
        options += ["--prefix={0}".format(prefix)]
        options += self.configure_args()

        with fs.working_dir(self.build_directory, create=True):
            Executable(join_path(self.stage.source_path, "libstdc++-v3", "configure"))(*options)


    # https://gcc.gnu.org/install/configure.html
    def configure_args(self):
        spec = self.spec

        # Generic options to compile GCC
        options = [
            # Distributor options
            "--with-pkgversion=Spack GCC",
            "--with-bugurl=https://github.com/spack/spack/issues",
            # Xcode 10 dropped 32-bit support
            "--disable-multilib",
            # Drop gettext dependency
            "--disable-nls",
            "--disable-bootstrap",
        ]

        sysroot_target = "{}-spack-linux-gnu".format(self.spec.architecture.target.microarchitecture.family.name)
        # Binutils
        if spec.satisfies("+binutils"):
            if "+stage1" not in self.spec:
                binutils = spec["binutils"].prefix.bin
            else:
                binutils = spec["binutils"].prefix.join(sysroot_target).bin
            options.extend(
                [
                    "--with-gnu-ld",
                    "--with-ld=" + binutils.ld,
                    "--with-gnu-as",
                    "--with-as=" + binutils.join("as"),
                ]
            )

        if "+stage1" in self.spec:
            # set up links to binutils, required for gcc to build this way
            glibc = self.spec['glibc']
            common_flags=(" ".join(['-isystem ' ,
                                             glibc.prefix.include,
                                             '-B ', glibc.prefix,
                                             "-B", glibc.prefix.lib, ]))
            options.extend(
                [
                    "--target=" + sysroot_target,
                    "--disable-libstdcxx-pch",
                    "--with-gxx-include-dir=" + self.prefix.include.join("c++"),
                    # NOTE(trws): we *must* set CFLAGS rather than CPPFLAGS or libtool
                    # will find the wrong c runtime objects from the compiler
                    'CFLAGS=' + common_flags,
                    'CXXFLAGS=' + common_flags,
                    'LDFLAGS=' + (" ".join([
                        "-Wl,-rpath," + glibc.prefix.lib,
                        "-Wl,--dynamic-linker," + glibc.prefix.lib.join("ld-linux-x86-64.so.2"),
                    ])),
                ]
            )
            return options

        # Avoid excessive realpath/stat calls for every system header
        # by making -fno-canonical-system-headers the default.
        if self.version >= Version("4.8.0"):
            options.append("--disable-canonical-system-headers")

        # Use installed libz
        if self.version >= Version("6"):
            options.append("--with-system-zlib")

        if "zstd" in spec:
            options.append("--with-zstd-include={0}".format(spec["zstd"].headers.directories[0]))
            options.append("--with-zstd-lib={0}".format(spec["zstd"].libs.directories[0]))

        # Enabling language "jit" requires --enable-host-shared.
        if "languages=jit" in spec:
            options.append("--enable-host-shared")

        # enable_bootstrap
        if spec.satisfies("+bootstrap"):
            options.extend(["--enable-bootstrap"])
        else:
            options.extend(["--disable-bootstrap"])

        # Configure include and lib directories explicitly for these
        # dependencies since the short GCC option assumes that libraries
        # are installed in "/lib" which might not be true on all OS
        # (see #10842)
        #
        # More info at: https://gcc.gnu.org/install/configure.html
        for dep_str in ("mpfr", "gmp", "mpc", "isl"):
            if dep_str not in spec:
                options.append("--without-{0}".format(dep_str))
                continue

            dep_spec = spec[dep_str]
            include_dir = dep_spec.headers.directories[0]
            lib_dir = dep_spec.libs.directories[0]
            options.extend(
                [
                    "--with-{0}-include={1}".format(dep_str, include_dir),
                    "--with-{0}-lib={1}".format(dep_str, lib_dir),
                ]
            )

        # enable appropriate bootstrapping flags
        stage1_ldflags = str(self.rpath_args)
        boot_ldflags = stage1_ldflags + " -static-libstdc++ -static-libgcc"
        options.append("--with-stage1-ldflags=" + stage1_ldflags)
        options.append("--with-boot-ldflags=" + boot_ldflags)
        options.append("--with-build-config=spack")

        return options
