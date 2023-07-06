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

import llnl.util.tty as tty
from llnl.util.lang import classproperty

import spack.platforms
import spack.util.executable
from spack.build_environment import dso_suffix
from spack.operating_systems.mac_os import macos_sdk_path, macos_version
from spack.package import *


class Gcc(AutotoolsPackage, GNUMirrorPackage):
    """The GNU Compiler Collection includes front ends for C, C++, Objective-C,
    Fortran, Ada, and Go, as well as libraries for these languages."""

    homepage = "https://gcc.gnu.org"
    gnu_mirror_path = "gcc/gcc-9.2.0/gcc-9.2.0.tar.xz"
    git = "git://gcc.gnu.org/git/gcc.git"
    list_url = "https://ftp.gnu.org/gnu/gcc/"
    list_depth = 1
    keep_werror = "all"

    maintainers("michaelkuhn", "alalazo")

    version("master", branch="master")

    version("13.1.0", sha256="61d684f0aa5e76ac6585ad8898a2427aade8979ed5e7f85492286c4dfc13ee86")

    version("12.3.0", sha256="949a5d4f99e786421a93b532b22ffab5578de7321369975b91aec97adfda8c3b")
    version("12.2.0", sha256="e549cf9cf3594a00e27b6589d4322d70e0720cdd213f39beb4181e06926230ff")
    version("12.1.0", sha256="62fd634889f31c02b64af2c468f064b47ad1ca78411c45abe6ac4b5f8dd19c7b")

    version("11.4.0", sha256="3f2db222b007e8a4a23cd5ba56726ef08e8b1f1eb2055ee72c1402cea73a8dd9")
    version("11.3.0", sha256="b47cf2818691f5b1e21df2bb38c795fac2cfbd640ede2d0a5e1c89e338a3ac39")
    version("11.2.0", sha256="d08edc536b54c372a1010ff6619dd274c0f1603aa49212ba20f7aa2cda36fa8b")
    version("11.1.0", sha256="4c4a6fb8a8396059241c2e674b85b351c26a5d678274007f076957afa1cc9ddf")

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

    # We specifically do not add 'all' variant here because:
    # (i) Ada, D, Go, Jit, and Objective-C++ are not default languages.
    # In that respect, the name 'all' is rather misleading.
    # (ii) Languages other than c,c++,fortran are prone to configure bug in GCC
    # For example, 'java' appears to ignore custom location of zlib
    # (iii) meaning of 'all' changes with GCC version, i.e. 'java' is not part
    # of gcc7. Correctly specifying conflicts() and depends_on() in such a
    # case is a PITA.
    #
    # Also note that some languages get enabled by the configure scripts even if not listed in the
    # arguments. For example, c++ is enabled when the bootstrapping is enabled and lto is enabled
    # when the link time optimization support is enabled.
    variant(
        "languages",
        default="c,c++,fortran",
        values=(
            "ada",
            "brig",
            "c",
            "c++",
            "d",
            "fortran",
            "go",
            "java",
            "jit",
            "lto",
            "objc",
            "obj-c++",
        ),
        multi=True,
        description="Compilers and runtime libraries to build",
    )
    variant("binutils", default=False, description="Build via binutils")
    variant(
        "piclibs", default=False, description="Build PIC versions of libgfortran.a and libstdc++.a"
    )
    variant("strip", default=False, description="Strip executables to reduce installation size")
    variant("nvptx", default=False, description="Target nvptx offloading to NVIDIA GPUs")
    variant("bootstrap", default=True, description="Enable 3-stage bootstrap")
    variant(
        "graphite", default=False, description="Enable Graphite loop optimizations (requires ISL)"
    )
    variant(
        "build_type",
        default="RelWithDebInfo",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
        description="CMake-like build type. "
        "Debug: -O0 -g; Release: -O3; "
        "RelWithDebInfo: -O2 -g; MinSizeRel: -Os",
    )
    variant(
        "profiled",
        default=False,
        description="Use Profile Guided Optimization",
        when="+bootstrap %gcc",
    )

    depends_on("flex", type="build", when="@master")

    # https://gcc.gnu.org/install/prerequisites.html
    depends_on("gmp@4.3.2:")
    # mawk is not sufficient for go support
    depends_on("gawk@3.1.5:", type="build")
    depends_on("texinfo@4.7:", type="build")
    depends_on("libtool", type="build")
    # dependencies required for git versions
    depends_on("m4@1.4.6:", when="@master", type="build")
    depends_on("automake@1.15.1:", when="@master", type="build")
    depends_on("autoconf@2.69:", when="@master", type="build")

    depends_on("gmake@3.80:", type="build")
    depends_on("perl@5", type="build")

    # GCC 7.3 does not compile with newer releases on some platforms, see
    #   https://github.com/spack/spack/issues/6902#issuecomment-433030376
    depends_on("mpfr@2.4.2:3.1.6", when="@:9.9")
    depends_on("mpfr@3.1.0:", when="@10:")
    depends_on("mpc@1.0.1:", when="@4.5:")
    # Already released GCC versions do not support any newer version of ISL
    #   GCC 5.4 https://github.com/spack/spack/issues/6902#issuecomment-433072097
    #   GCC 7.3 https://github.com/spack/spack/issues/6902#issuecomment-433030376
    #   GCC 9+  https://gcc.gnu.org/bugzilla/show_bug.cgi?id=86724
    with when("+graphite"):
        depends_on("isl@0.14", when="@5.0:5.2")
        depends_on("isl@0.15", when="@5.3:5.9")
        depends_on("isl@0.15:0.18", when="@6:8.9")
        depends_on("isl@0.15:0.20", when="@9:9.9")
        depends_on("isl@0.15:", when="@10:")

    depends_on("zlib", when="@6:")
    depends_on("zstd", when="@10:")
    depends_on("diffutils", type="build")
    depends_on("iconv", when="platform=darwin")
    depends_on("gnat", when="languages=ada")
    depends_on(
        "binutils+gas+ld+plugins~libiberty", when="+binutils", type=("build", "link", "run")
    )
    depends_on("zip", type="build", when="languages=java")

    # The server is sometimes a bit slow to respond
    timeout = {"timeout": 60}

    # TODO: integrate these libraries.
    # depends_on('ppl')
    # depends_on('cloog')

    # https://gcc.gnu.org/install/test.html
    depends_on("dejagnu@1.4.4", type="test")
    depends_on("expect", type="test")
    depends_on("tcl", type="test")
    depends_on("autogen@5.5.4:", type="test")
    depends_on("guile@1.4.1:", type="test")

    # See https://go.dev/doc/install/gccgo#Releases
    with when("languages=go"):
        provides("go-or-gccgo-bootstrap@:1.0", when="@4.7.1:")
        provides("go-or-gccgo-bootstrap@:1.2", when="@4.9:")
        provides("go-or-gccgo-bootstrap@:1.4", when="@5:")
        provides("go-or-gccgo-bootstrap@:1.6.1", when="@6:")
        provides("go-or-gccgo-bootstrap@:1.8.1", when="@7:")
        provides("go-or-gccgo-bootstrap@:1.10.1", when="@8:")
        provides("go-or-gccgo-bootstrap@:1.12.2", when="@9:")
        provides("go-or-gccgo-bootstrap@:1.14.6", when="@10:")
        provides("go-or-gccgo-bootstrap@1.16.3:1.16.5", when="@11:")

        provides("golang@:1.0", when="@4.7.1:")
        provides("golang@:1.2", when="@4.9:")
        provides("golang@:1.4", when="@5:")
        provides("golang@:1.6.1", when="@6:")
        provides("golang@:1.8.1", when="@7:")
        provides("golang@:1.10.1", when="@8:")
        provides("golang@:1.12.2", when="@9:")
        provides("golang@:1.14.6", when="@10:")
        provides("golang@1.16.3:1.16.5", when="@11:")

        # GCC 4.7.1 added full support for the Go 1.x programming language.
        conflicts("@:4.7.0")

        # Go is not supported on macOS
        conflicts("platform=darwin", msg="GCC cannot build Go support on MacOS")

    # For a list of valid languages for a specific release,
    # run the following command in the GCC source directory:
    #    $ grep ^language= gcc/*/config-lang.in
    # See https://gcc.gnu.org/install/configure.html

    # Support for processing BRIG 1.0 files was added in GCC 7
    # BRIG is a binary format for HSAIL:
    # (Heterogeneous System Architecture Intermediate Language).
    # See https://gcc.gnu.org/gcc-7/changes.html
    conflicts("languages=brig", when="@:6")

    # BRIG does not seem to be supported on macOS
    conflicts("languages=brig", when="platform=darwin")

    # GCC 4.8 added a 'c' language. I'm sure C was always built,
    # but this is the first version that accepts 'c' as a valid language.
    conflicts("languages=c", when="@:4.7")

    # The GCC Java frontend and associated libjava runtime library
    # have been removed from GCC as of GCC 7.
    # See https://gcc.gnu.org/gcc-7/changes.html
    conflicts("languages=java", when="@7:")

    # GCC 5 added the ability to build GCC as a Just-In-Time compiler.
    # See https://gcc.gnu.org/gcc-5/changes.html
    conflicts("languages=jit", when="@:4")

    with when("languages=d"):
        # The very first version of GDC that became part of GCC already supported version 2.076 of
        # the language and runtime.
        # See https://wiki.dlang.org/GDC#Status
        provides("D@2")

        # Support for the D programming language has been added to GCC 9.
        # See https://gcc.gnu.org/gcc-9/changes.html#d
        conflicts("@:8", msg="support for D has been added in GCC 9.1")

        # Versions of GDC prior to 12 can be built with an ISO C++11 compiler. Starting version 12,
        # the D frontend requires a working GDC. Moreover, it is strongly recommended to use an
        # older version of GDC to build GDC.
        # See https://gcc.gnu.org/install/prerequisites.html#GDC-prerequisite
        with when("@12:"):
            # All versions starting 12 have to be built GCC:
            requires("%gcc")

            # And it has to be GCC older than the version we build:
            vv = ["11", "12.1.0", "12.2.0"]
            for prev_v, curr_v in zip(vv, vv[1:]):
                conflicts(
                    "%gcc@{0}:".format(curr_v),
                    when="@{0}".format(curr_v),
                    msg="'gcc@{0} languages=d' requires '%gcc@:{1}' "
                    "with the D language support".format(curr_v, prev_v),
                )

            # In principle, it is possible to have GDC even with GCC 5.
            # See https://github.com/D-Programming-GDC/gdc
            # We, however, require at least the oldest version that officially supports GDC. It is
            # also a good opportunity to tell the users that they need a working GDC:
            conflicts(
                "%gcc@:8",
                msg="'gcc@12: languages=d' requires '%gcc@9:' with the D language support",
            )

    with when("+nvptx"):
        depends_on("cuda")
        resource(
            name="newlib",
            url="ftp://sourceware.org/pub/newlib/newlib-3.0.0.20180831.tar.gz",
            sha256="3ad3664f227357df15ff34e954bfd9f501009a647667cd307bf0658aefd6eb5b",
            destination="newlibsource",
            fetch_options=timeout,
        )
        # nvptx-tools does not seem to work as a dependency,
        # but does fine when the source is inside the gcc build directory
        # nvptx-tools doesn't have any releases, so grabbing the last commit
        resource(
            name="nvptx-tools",
            git="https://github.com/MentorEmbedded/nvptx-tools",
            commit="d0524fbdc86dfca068db5a21cc78ac255b335be5",
        )
        # NVPTX offloading supported in 7 and later by limited languages
        conflicts("@:6", msg="NVPTX only supported in gcc 7 and above")
        conflicts("languages=ada")
        conflicts("languages=brig")
        conflicts("languages=go")
        conflicts("languages=java")
        conflicts("languages=jit")
        conflicts("languages=objc")
        conflicts("languages=obj-c++")
        conflicts("languages=d")
        # NVPTX build disables bootstrap
        conflicts("+bootstrap")

    # Binutils can't build ld on macOS
    conflicts("+binutils", when="platform=darwin")

    # Bootstrap comparison failure:
    #   see https://github.com/spack/spack/issues/23296
    #   https://gcc.gnu.org/bugzilla/show_bug.cgi?id=100340
    #   on XCode 12.5
    conflicts("+bootstrap", when="@:11.1 %apple-clang@12.0.5")

    # aarch64/M1 is supported in GCC 11.3-12.2
    conflicts(
        "@:11.2,12.3:",
        when="target=aarch64: platform=darwin",
        msg="Only GCC 11.3-12.2 support macOS M1 (aarch64)",
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

    if sys.platform == "darwin":
        # Fix parallel build on APFS filesystem
        # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=81797
        if macos_version() >= Version("10.13"):
            patch("darwin/apfs.patch", when="@5.5.0,6.1:6.4,7.1:7.3")
            # from homebrew via macports
            # https://trac.macports.org/ticket/56502#no1
            # see also: https://gcc.gnu.org/bugzilla/show_bug.cgi?id=83531
            patch("darwin/headers-10.13-fix.patch", when="@5.5.0")
        if macos_version() >= Version("10.14"):
            # Fix system headers for Mojave SDK:
            # https://github.com/Homebrew/homebrew-core/pull/39041
            patch(
                "https://raw.githubusercontent.com/Homebrew/formula-patches/b8b8e65e/gcc/8.3.0-xcode-bug-_Atomic-fix.patch",
                sha256="33ee92bf678586357ee8ab9d2faddf807e671ad37b97afdd102d5d153d03ca84",
                when="@6:8.3",
            )
        if macos_version() >= Version("10.15"):
            # Fix system headers for Catalina SDK
            # (otherwise __OSX_AVAILABLE_STARTING ends up undefined)
            patch(
                "https://raw.githubusercontent.com/Homebrew/formula-patches/b8b8e65e/gcc/9.2.0-catalina.patch",
                sha256="0b8d14a7f3c6a2f0d2498526e86e088926671b5da50a554ffa6b7f73ac4f132b",
                when="@9.2.0",
            )

            # See https://raw.githubusercontent.com/Homebrew/homebrew-core/3b7db4457ac64a31e3bbffc54b04c4bd824a4a4a/Formula/gcc.rb
            patch(
                "https://github.com/iains/gcc-darwin-arm64/commit/20f61faaed3b335d792e38892d826054d2ac9f15.patch?full_index=1",
                sha256="c0605179a856ca046d093c13cea4d2e024809ec2ad4bf3708543fc3d2e60504b",
                when="@11.2.0",
            )

        # Apple M1 support, created from branch of Darwin maintainer for GCC:
        # https://github.com/iains/gcc-11-branch
        patch(
            "https://raw.githubusercontent.com/Homebrew/formula-patches/22dec3fc/gcc/gcc-11.3.0-arm.diff",
            sha256="e02006b7ec917cc1390645d95735a6a866caed0dfe506d5bef742f7862cab218",
            when="@11.3.0 target=aarch64:",
        )
        # https://github.com/iains/gcc-12-branch
        patch(
            "https://raw.githubusercontent.com/Homebrew/formula-patches/76677f2b/gcc/gcc-12.1.0-arm.diff",
            sha256="a000f1d9cb1dd98c7c4ef00df31435cd5d712d2f9d037ddc044f8bf82a16cf35",
            when="@12.1.0 target=aarch64:",
        )
        patch(
            "https://raw.githubusercontent.com/Homebrew/formula-patches/1d184289/gcc/gcc-12.2.0-arm.diff",
            sha256="a7843b5c6bf1401e40c20c72af69c8f6fc9754ae980bb4a5f0540220b3dcb62d",
            when="@12.2.0 target=aarch64:",
        )
        conflicts("+bootstrap", when="@11.3.0 target=aarch64:")

        # Use -headerpad_max_install_names in the build,
        # otherwise updated load commands won't fit in the Mach-O header.
        # This is needed because `gcc` avoids the superenv shim.
        patch("darwin/gcc-7.1.0-headerpad.patch", when="@5:11.2")
        patch("darwin/gcc-6.1.0-jit.patch", when="@5:7")
        patch("darwin/gcc-4.9.patch1", when="@4.9.0:4.9.3")
        patch("darwin/gcc-4.9.patch2", when="@4.9.0:4.9.3")

        # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=92061
        patch("darwin/clang13.patch", when="@:11.1 %apple-clang@13")

    patch("piclibs.patch", when="+piclibs")
    patch("gcc-backport.patch", when="@4.7:4.9.3,5:5.3")

    # Backport libsanitizer patch for glibc >= 2.31 and 5.3.0 <= gcc <= 9.2.0
    # https://bugs.gentoo.org/708346
    patch("glibc-2.31-libsanitizer-1.patch", when="@7.1.0:7.5.0,8.1.0:8.3.0,9.0.0:9.2.0")
    patch("glibc-2.31-libsanitizer-1-gcc-6.patch", when="@5.3.0:5.5.0,6.1.0:6.5.0")
    patch("glibc-2.31-libsanitizer-2.patch", when="@8.1.0:8.3.0,9.0.0:9.2.0")
    patch("glibc-2.31-libsanitizer-2-gcc-6.patch", when="@5.3.0:5.5.0,6.1.0:6.5.0")
    patch("glibc-2.31-libsanitizer-2-gcc-7.patch", when="@7.1.0:7.5.0")
    patch(
        "patch-2b40941d23b1570cdd90083b58fa0f66aa58c86e.patch",
        when="@6.5.0,7.4.0:7.5.0,8.2.0:9.3.0",
    )
    patch("patch-745dae5923aba02982563481d75a21595df22ff8.patch", when="@10.1.0:10.3.0,11.1.0")

    # Backport libsanitizer patch for glibc >= 2.36
    # https://reviews.llvm.org/D129471
    patch("glibc-2.36-libsanitizer-gcc-5-9.patch", when="@5.1:5.5,6.1:6.5,7.1:7.5,8.1:8.5,9.1:9.5")
    patch("glibc-2.36-libsanitizer-gcc-10-12.patch", when="@10.1:10.4,11.1:11.3,12.1.0")

    # Older versions do not compile with newer versions of glibc
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=81712
    patch("ucontext_t.patch", when="@4.9,5.1:5.4,6.1:6.4,7.1")
    patch("ucontext_t-java.patch", when="@4.9,5.1:5.4,6.1:6.4 languages=java")
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=81066
    patch("stack_t-4.9.patch", when="@4.9")
    patch("stack_t.patch", when="@5.1:5.4,6.1:6.4,7.1")
    # https://bugs.busybox.net/show_bug.cgi?id=10061
    patch("signal.patch", when="@4.9,5.1:5.4")
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=85835
    patch("sys_ustat.h.patch", when="@5.0:6.4,7.0:7.3,8.1")
    patch("sys_ustat-4.9.patch", when="@4.9")

    # this patch removes cylades support from gcc-5 and allows gcc-5 to be built
    # with newer glibc versions.
    patch("glibc-2.31-libsanitizer-3-gcc-5.patch", when="@5.3.0:5.5.0")

    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=95005
    patch("zstd.patch", when="@10")

    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=100102
    patch("patch-fc930b3010bd0de899a3da3209eab20664ddb703.patch", when="@10.1:10.3")
    patch("patch-f1feb74046e0feb0596b93bbb822fae02940a90e.patch", when="@11.1")

    # libstdc++: Fix inconsistent noexcept-specific for valarray begin/end
    patch(
        "https://github.com/gcc-mirror/gcc/commit/423cd47cfc9640ba3d6811b780e8a0b94b704dcb.patch?full_index=1",
        sha256="0d136226eb07bc43f1b15284f48bd252e3748a0426b5d7ac9084ebc406e15490",
        when="@9.5.0:11.2",
    )

    build_directory = "spack-build"

    @classproperty
    def executables(cls):
        names = [r"gcc", r"[^\w]?g\+\+", r"gfortran", r"gdc", r"gccgo"]
        suffixes = [r"", r"-mp-\d+\.\d", r"-\d+\.\d", r"-\d+", r"\d\d"]
        return [r"".join(x) for x in itertools.product(names, suffixes)]

    @classmethod
    def filter_detected_exes(cls, prefix, exes_in_prefix):
        result = []
        for exe in exes_in_prefix:
            # On systems like Ubuntu we might get multiple executables
            # with the string "gcc" in them. See:
            # https://helpmanual.io/packages/apt/gcc/
            basename = os.path.basename(exe)
            substring_to_be_filtered = [
                "c99-gcc",
                "c89-gcc",
                "-nm",
                "-ar",
                "ranlib",
                "clang",  # clang++ matches g++ -> clan[g++]
            ]
            if any(x in basename for x in substring_to_be_filtered):
                continue
            # Filter out links in favor of real executables on
            # all systems but Cray
            host_platform = str(spack.platforms.host())
            if os.path.islink(exe) and host_platform != "cray":
                continue

            result.append(exe)

        return result

    @classmethod
    def determine_version(cls, exe):
        try:
            output = spack.compiler.get_compiler_version_output(exe, "--version")
        except Exception:
            output = ""
        # Apple's gcc is actually apple clang, so skip it.
        # Users can add it manually to compilers.yaml at their own risk.
        if "Apple" in output:
            return None

        version_regex = re.compile(r"([\d\.]+)")
        for vargs in ("-dumpfullversion", "-dumpversion"):
            try:
                output = spack.compiler.get_compiler_version_output(exe, vargs)
                match = version_regex.search(output)
                if match:
                    return match.group(1)
            except spack.util.executable.ProcessError:
                pass
            except Exception as e:
                tty.debug(e)

        return None

    @classmethod
    def determine_variants(cls, exes, version_str):
        languages, compilers = set(), {}
        # There are often at least two copies (not symlinks) of each compiler executable in the
        # same directory: one with a canonical name, e.g. "gfortran", and another one with the
        # target prefix, e.g. "x86_64-pc-linux-gnu-gfortran". There also might be a copy of "gcc"
        # with the version suffix, e.g. "x86_64-pc-linux-gnu-gcc-6.3.0". To ensure the consistency
        # of values in the "compilers" dictionary (i.e. we prefer all of them to reference copies
        # with canonical names if possible), we iterate over the executables in the reversed sorted
        # order:
        for exe in sorted(exes, reverse=True):
            basename = os.path.basename(exe)
            if "g++" in basename:
                languages.add("c++")
                compilers["cxx"] = exe
            elif "gfortran" in basename:
                languages.add("fortran")
                compilers["fortran"] = exe
            elif "gcc" in basename:
                languages.add("c")
                compilers["c"] = exe
            elif "gccgo" in basename:
                languages.add("go")
                compilers["go"] = exe
            elif "gdc" in basename:
                languages.add("d")
                compilers["d"] = exe
        variant_str = "languages={0}".format(",".join(languages))
        return variant_str, {"compilers": compilers}

    @classmethod
    def validate_detected_spec(cls, spec, extra_attributes):
        # For GCC 'compilers' is a mandatory attribute
        msg = 'the extra attribute "compilers" must be set for ' 'the detected spec "{0}"'.format(
            spec
        )
        assert "compilers" in extra_attributes, msg

        compilers = extra_attributes["compilers"]
        for constraint, key in {
            "languages=c": "c",
            "languages=c++": "cxx",
            "languages=d": "d",
            "languages=fortran": "fortran",
        }.items():
            if spec.satisfies(constraint):
                msg = "{0} not in {1}"
                assert key in compilers, msg.format(key, spec)

    @property
    def cc(self):
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("c", None)
        result = None
        if "languages=c" in self.spec:
            result = str(self.spec.prefix.bin.gcc)
        return result

    @property
    def cxx(self):
        msg = "cannot retrieve C++ compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("cxx", None)
        result = None
        if "languages=c++" in self.spec:
            result = os.path.join(self.spec.prefix.bin, "g++")
        return result

    @property
    def fortran(self):
        msg = "cannot retrieve Fortran compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("fortran", None)
        result = None
        if "languages=fortran" in self.spec:
            result = str(self.spec.prefix.bin.gfortran)
        return result

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

    def patch(self):
        spec = self.spec
        prefix = self.spec.prefix

        # Fix a standard header file for OS X Yosemite that
        # is GCC incompatible by replacing non-GCC compliant macros
        if "yosemite" in spec.architecture:
            if os.path.isfile("/usr/include/dispatch/object.h"):
                new_dispatch_dir = join_path(prefix, "include", "dispatch")
                mkdirp(new_dispatch_dir)
                new_header = join_path(new_dispatch_dir, "object.h")
                install("/usr/include/dispatch/object.h", new_header)
                filter_file(
                    r"typedef void \(\^dispatch_block_t\)\(void\)",
                    "typedef void* dispatch_block_t",
                    new_header,
                )

        # Use installed libz
        if self.version >= Version("6"):
            filter_file("@zlibdir@", "-L{0}".format(spec["zlib"].prefix.lib), "gcc/Makefile.in")
            filter_file(
                "@zlibinc@", "-I{0}".format(spec["zlib"].prefix.include), "gcc/Makefile.in"
            )

        if spec.satisfies("+nvptx"):
            # backport of 383400a6078d upstream to allow support of cuda@11:
            filter_file(
                '#define ASM_SPEC "%{misa=*:-m %*}"',
                '#define ASM_SPEC "%{misa=*:-m %*; :-m sm_35}"',
                "gcc/config/nvptx/nvptx.h",
                string=True,
            )
            filter_file(
                "Target RejectNegative ToLower Joined "
                "Enum(ptx_isa) Var(ptx_isa_option) Init(PTX_ISA_SM30)",
                "Target RejectNegative ToLower Joined "
                "Enum(ptx_isa) Var(ptx_isa_option) Init(PTX_ISA_SM35)",
                "gcc/config/nvptx/nvptx.opt",
                string=True,
            )
        self.build_optimization_config()

    def get_common_target_flags(self, spec):
        """Get the right (but pessimistic) architecture specific flags supported by
        both host gcc and to-be-built gcc. For example: gcc@7 %gcc@12 target=znver3
        should pick -march=znver1, since that's what gcc@7 supports."""
        archs = [spec.target] + spec.target.ancestors
        for arch in archs:
            try:
                return arch.optimization_flags("gcc", spec.version)
            except UnsupportedMicroarchitecture:
                pass
        # no arch specific flags in common, unlikely to happen.
        return ""

    def build_optimization_config(self):
        """Write a config/spack.mk file with sensible optimization flags, taking into
        account bootstrapping subtleties."""
        build_type_flags = {
            "Debug": "-O0 -g",
            "Release": "-O3",
            "RelWithDebInfo": "-O2 -g",
            "MinSizeRel": "-Os",
        }

        # Generic optimization flags.
        flags = build_type_flags[self.spec.variants["build_type"].value]

        # Pessimistic target specific flags. For example, when building
        # gcc@11 %gcc@7 on znver3, Spack will fix the target to znver1 during
        # concretization, so we'll stick to that. The other way around however can
        # result in compilation errors, when gcc@7 is built with gcc@11, and znver3
        # is taken as a the target, which gcc@7 doesn't support.
        # Note we're not adding this for aarch64 because of
        # https://github.com/spack/spack/issues/31184
        if "+bootstrap %gcc" in self.spec and self.spec.target.family != "aarch64":
            flags += " " + self.get_common_target_flags(self.spec)

        if "+bootstrap" in self.spec:
            variables = ["BOOT_CFLAGS", "CFLAGS_FOR_TARGET", "CXXFLAGS_FOR_TARGET"]
        else:
            variables = ["CFLAGS", "CXXFLAGS"]

        # Redefine a few variables without losing other defaults:
        # BOOT_CFLAGS = $(filter-out -O% -g%, $(BOOT_CFLAGS)) -O3
        # This makes sure that build_type=Release is really -O3, not -O3 -g.
        fmt_string = "{} := $(filter-out -O% -g%, $({})) {}\n"
        with open("config/spack.mk", "w") as f:
            for var in variables:
                f.write(fmt_string.format(var, var, flags))
            # Improve the build time for stage 2 a bit by enabling -O1 in stage 1.
            # Note: this is ignored under ~bootstrap.
            f.write("STAGE1_CFLAGS += -O1\n")

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
            "--enable-languages={0}".format(",".join(spec.variants["languages"].value)),
            # Drop gettext dependency
            "--disable-nls",
        ]

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

        # Binutils
        if spec.satisfies("+binutils"):
            binutils = spec["binutils"].prefix.bin
            options.extend(
                [
                    "--with-gnu-ld",
                    "--with-ld=" + binutils.ld,
                    "--with-gnu-as",
                    "--with-as=" + binutils.join("as"),
                ]
            )

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

        # nvptx-none offloading for host compiler
        if spec.satisfies("+nvptx"):
            options.extend(
                [
                    "--enable-offload-targets=nvptx-none",
                    "--with-cuda-driver-include={0}".format(spec["cuda"].prefix.include),
                    "--with-cuda-driver-lib={0}".format(spec["cuda"].libs.directories[0]),
                    "--disable-bootstrap",
                    "--disable-multilib",
                ]
            )

        if sys.platform == "darwin":
            options.extend(
                [
                    "--with-native-system-header-dir=/usr/include",
                    "--with-sysroot={0}".format(macos_sdk_path()),
                    "--with-libiconv-prefix={0}".format(spec["iconv"].prefix),
                ]
            )

        # enable appropriate bootstrapping flags
        stage1_ldflags = str(self.rpath_args)
        boot_ldflags = stage1_ldflags + " -static-libstdc++ -static-libgcc"
        options.append("--with-stage1-ldflags=" + stage1_ldflags)
        options.append("--with-boot-ldflags=" + boot_ldflags)
        options.append("--with-build-config=spack")

        if "languages=d" in spec:
            # Phobos is the standard library for the D Programming Language. The documentation says
            # that on some targets, 'libphobos' is not enabled by default, but compiles and works
            # if '--enable-libphobos' is used. Specifics are documented for affected targets.
            # See https://gcc.gnu.org/install/prerequisites.html#GDC-prerequisite
            # Unfortunately, it is unclear where exactly the aforementioned specifics are
            # documented but GDC seems to be unusable without the library, therefore we enable it
            # explicitly:
            options.append("--enable-libphobos")
            if spec.satisfies("@12:"):
                options.append("GDC={0}".format(self.detect_gdc()))

        return options

    # run configure/make/make(install) for the nvptx-none target
    # before running the host compiler phases
    @run_before("configure")
    def nvptx_install(self):
        spec = self.spec
        prefix = self.prefix

        if not spec.satisfies("+nvptx"):
            return

        # config.guess returns the host triple, e.g. "x86_64-pc-linux-gnu"
        guess = Executable("./config.guess")
        targetguess = guess(output=str).rstrip("\n")

        options = getattr(self, "configure_flag_args", [])
        options += ["--prefix={0}".format(prefix)]

        options += [
            "--with-cuda-driver-include={0}".format(spec["cuda"].prefix.include),
            "--with-cuda-driver-lib={0}".format(spec["cuda"].libs.directories[0]),
        ]

        with working_dir("nvptx-tools"):
            configure = Executable("./configure")
            configure(*options)
            make()
            make("install")

        pattern = join_path(self.stage.source_path, "newlibsource", "*")
        files = glob.glob(pattern)

        if files:
            symlink(join_path(files[0], "newlib"), "newlib")

        # self.build_directory = 'spack-build-nvptx'
        with working_dir("spack-build-nvptx", create=True):
            options = [
                "--prefix={0}".format(prefix),
                "--enable-languages={0}".format(",".join(spec.variants["languages"].value)),
                "--with-mpfr={0}".format(spec["mpfr"].prefix),
                "--with-gmp={0}".format(spec["gmp"].prefix),
                "--target=nvptx-none",
                "--with-build-time-tools={0}".format(join_path(prefix, "nvptx-none", "bin")),
                "--enable-as-accelerator-for={0}".format(targetguess),
                "--disable-sjlj-exceptions",
                "--enable-newlib-io-long-long",
            ]

            configure = Executable("../configure")
            configure(*options)
            make()
            make("install")

    @property
    def build_targets(self):
        if "+profiled" in self.spec:
            return ["profiledbootstrap"]
        return []

    @property
    def install_targets(self):
        if "+strip" in self.spec:
            return ["install-strip"]
        return ["install"]

    @property
    def spec_dir(self):
        # e.g. lib/gcc/x86_64-unknown-linux-gnu/4.9.2
        spec_dir = glob.glob("{0}/gcc/*/*".format(self.prefix.lib))
        return spec_dir[0] if spec_dir else None

    @run_after("install")
    def write_rpath_specs(self):
        """Generate a spec file so the linker adds a rpath to the libs
        the compiler used to build the executable.

        .. caution::

           The custom spec file by default with *always* pass ``-Wl,-rpath
           ...`` to the linker, which will cause the linker to *ignore* the
           value of ``LD_RUN_PATH``, which otherwise would be saved to the
           binary as the default rpath. See the mitigation below for how to
           temporarily disable this behavior.

        Structure the specs file so that users can define a custom spec file
        to suppress the spack-linked rpaths to facilitate rpath adjustment
        for relocatable binaries. The custom spec file
        :file:`{norpath}.spec` will have a single
        line followed by two blanks lines::

            *link_libgcc_rpath:



        It can be passed to the GCC linker using the argument
        ``--specs=norpath.spec`` to disable the automatic rpath and restore
        the behavior of ``LD_RUN_PATH``."""
        if not self.spec_dir:
            tty.warn(
                "Could not install specs for {0}.".format(self.spec.format("{name}{@version}"))
            )
            return

        gcc = self.spec["gcc"].command
        lines = gcc("-dumpspecs", output=str).splitlines(True)
        specs_file = join_path(self.spec_dir, "specs")

        # Save a backup
        with open(specs_file + ".orig", "w") as out:
            out.writelines(lines)

        # Find which directories have shared libraries
        rpath_libdirs = []
        for dir in ["lib", "lib64"]:
            libdir = join_path(self.prefix, dir)
            if glob.glob(join_path(libdir, "*." + dso_suffix)):
                rpath_libdirs.append(libdir)

        if not rpath_libdirs:
            # No shared libraries
            tty.warn("No dynamic libraries found in lib/lib64")
            return

        # Overwrite the specs file
        with open(specs_file, "w") as out:
            for line in lines:
                out.write(line)
                if line.startswith("*link_libgcc:"):
                    # Insert at start of line following link_libgcc, which gets
                    # inserted into every call to the linker
                    out.write("%(link_libgcc_rpath) ")

            # Add easily-overridable rpath string at the end
            out.write("*link_libgcc_rpath:\n")
            out.write(" ".join("-rpath " + lib for lib in rpath_libdirs))
            out.write("\n")
        set_install_permissions(specs_file)
        tty.info("Wrote new spec file to {0}".format(specs_file))

    def setup_run_environment(self, env):
        # Search prefix directory for possibly modified compiler names
        from spack.compilers.gcc import Gcc as Compiler

        # Get the contents of the installed binary directory
        bin_path = self.spec.prefix.bin

        if not os.path.isdir(bin_path):
            return

        bin_contents = os.listdir(bin_path)

        # Find the first non-symlink compiler binary present for each language
        for lang in ["cc", "cxx", "fc", "f77"]:
            for filename, regexp in itertools.product(bin_contents, Compiler.search_regexps(lang)):
                if not regexp.match(filename):
                    continue

                abspath = os.path.join(bin_path, filename)
                if os.path.islink(abspath):
                    continue

                # Set the proper environment variable
                env.set(lang.upper(), abspath)
                # Stop searching filename/regex combos for this language
                break

    def detect_gdc(self):
        """Detect and return the path to GDC that belongs to the same instance of GCC that is used
        by self.compiler.

        If the path cannot be detected, raise InstallError with recommendations for the users on
        how to circumvent the problem.

        Should be use only if self.spec.satisfies("@12: languages=d")
        """
        # Detect GCC package in the directory of the GCC compiler
        # or in the $PATH if self.compiler.cc is not an absolute path:
        from spack.detection import by_executable

        compiler_dir = os.path.dirname(self.compiler.cc)
        detected_packages = by_executable(
            [self.__class__], path_hints=([compiler_dir] if os.path.isdir(compiler_dir) else None)
        )

        # We consider only packages that satisfy the following constraint:
        required_spec = Spec("languages=c,c++,d")
        candidate_specs = [
            p.spec
            for p in filter(
                lambda p: p.spec.satisfies(required_spec), detected_packages.get(self.name, ())
            )
        ]

        if candidate_specs:
            # We now need to filter specs that match the compiler version:
            compiler_spec = Spec(repr(self.compiler.spec))

            # First, try to filter specs that satisfy the compiler spec:
            new_candidate_specs = list(
                filter(lambda s: s.satisfies(compiler_spec), candidate_specs)
            )

            # The compiler version might be more specific than what we can detect. For example, the
            # user might have "gcc@10.2.1-sys" as the compiler spec in compilers.yaml. In that
            # case, we end up with an empty list of candidates. To circumvent the problem, we try
            # to filter specs that are satisfied by the compiler spec:
            if not new_candidate_specs:
                new_candidate_specs = list(
                    filter(lambda s: compiler_spec.satisfies(s), candidate_specs)
                )

            candidate_specs = new_candidate_specs

        error_nl = "\n    "  # see SpackError.__str__()

        if not candidate_specs:
            raise InstallError(
                "Cannot detect GDC",
                long_msg="Starting version 12, the D frontend requires a working GDC."
                "{0}You can install it with Spack by running:"
                "{0}{0}spack install gcc@9:11 languages=c,c++,d"
                "{0}{0}Once that has finished, you will need to add it to your compilers.yaml file"
                "{0}and use it to install this spec (i.e. {1} ...).".format(
                    error_nl, self.spec.format("{name}{@version} {variants.languages}")
                ),
            )
        elif len(candidate_specs) == 0:
            return candidate_specs[0].extra_attributes["compilers"]["d"]
        else:
            # It is rather unlikely to end up here but let us try to resolve the ambiguity:
            candidate_gdc = candidate_specs[0].extra_attributes["compilers"]["d"]
            if all(
                candidate_gdc == s.extra_attributes["compilers"]["d"] for s in candidate_specs[1:]
            ):
                # It does not matter which one we take if they are all the same:
                return candidate_gdc
            else:
                raise InstallError(
                    "Cannot resolve ambiguity when detecting GDC that belongs to "
                    "%{0}".format(self.compiler.spec),
                    long_msg="The candidates are:{0}{0}{1}{0}".format(
                        error_nl,
                        error_nl.join(
                            "{0} (cc: {1})".format(
                                s.extra_attributes["compilers"]["d"],
                                s.extra_attributes["compilers"]["c"],
                            )
                            for s in candidate_specs
                        ),
                    ),
                )
