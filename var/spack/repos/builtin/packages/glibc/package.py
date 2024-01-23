# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.build_systems.autotools import AutotoolsPackageNoDep
from spack.build_systems.gnu import GNUMirrorPackageNoDep

from spack.package import *
from spack.util.elf import delete_rpath


class Glibc(AutotoolsPackageNoDep, GNUMirrorPackageNoDep):
    """The GNU C Library provides many of the low-level components used
    directly by programs written in the C or C++ languages."""

    homepage = "https://www.gnu.org/software/libc/"
    gnu_mirror_path = "libc/glibc-2.33.tar.gz"
    git = "https://sourceware.org/git/glibc.git"
    tags = ["build-tools", "runtime"]

    maintainers("haampie")

    build_directory = "build"

    license("LGPL-2.1-or-later")

    version("master", branch="master")
    version("2.38", sha256="16e51e0455e288f03380b436e41d5927c60945abd86d0c9852b84be57dd6ed5e")
    version("2.37", sha256="e3a790c2f84eed5c5d569ed6172c253c607dd3962135437da413aa39aa4fd352")
    version("2.36", sha256="02efa6ffbbaf3e10e88f16818a862608d04b0ef838c66f6025ae120530792c9c")
    version("2.35", sha256="3e8e0c6195da8dfbd31d77c56fb8d99576fb855fafd47a9e0a895e51fd5942d4")
    version("2.34", sha256="255b7632746b5fdd478cb7b36bebd1ec1f92c2b552ee364c940f48eb38d07f62")
    version("2.33", sha256="ad7dbed6b0cde9ddc90e84856da7e2c1f976a5e791cdee947d8dbb0392fc76cf")
    version("2.32", sha256="f52e5bdc6607cb692c0f7134b75b3ba34b5121628a1750c03e3c9aa0b9d9e65a")
    version("2.31", sha256="cb2d64fb808affff30d8a99a85de9d2aa67dc2cbac4ae99af4500d6cfea2bda7")
    version("2.30", sha256="decb0a29f1410735bed0e8e7247361da2bbf0dcfef7ac15bf26e7f910cb964c0")
    version("2.29", sha256="2fc8c555fd0e5dab5b91e7dd0422865c1885be89ff080b2c1357041afbbc717f")
    version("2.28", sha256="f318d6e3f1f4ed0b74d2832ac4f491d0fb928e451c9eda594cbf1c3bee7af47c")
    version("2.27", sha256="881ca905e6b5eec724de7948f14d66a07d97bdee8013e1b2a7d021ff5d540522")
    version("2.26", sha256="dcc2482b00fdb1c316f385f8180e182bbd37c065dc7d8281a4339d2834ef1be7")
    version("2.25", sha256="ad984bac07844ecc222039d43bd5f1f1e1571590ea28045232ae3fa404cefc32")
    version("2.24", sha256="7e01959a42d37739e40d8ce58f9c14750cc68bc8a8669889ed586f9f03b91fbe")
    version("2.23", sha256="2bd08abb24811cda62e17e61e9972f091f02a697df550e2e44ddcfb2255269d2")
    version("2.22", sha256="a62610c4084a0fd8cec58eee12ef9e61fdf809c31e7cecbbc28feb8719f08be5")
    version("2.21", sha256="8d8f78058f2e9c7237700f76fe4e0ae500db31470290cd0b8a9739c0c8ce9738")
    version("2.20", sha256="37e1de410d572a19b707b99786db9822bb4775e9d70517d88937ab12e6d6debc")
    version("2.19", sha256="18ad6db70724699d264add80b1f813630d0141cf3a3558b4e1a7c15f6beac796")
    version("2.18", sha256="c8e727b5feef883184241a4767725ec280c0288794bc5cd4432497370db47734")
    version("2.17", sha256="a3b2086d5414e602b4b3d5a8792213feb3be664ffc1efe783a829818d3fca37a")
    version("2.16.0", sha256="a75be51658cc1cfb6324ec6dbdbed416526c44c14814823129f0fcc74c279f6e")
    version("2.15", sha256="da6b95d14b722539c2ec02e7ae1221318dba3d27f19c098a882ffa71bb429c20")
    version("2.14.1", sha256="f80c40897df49c463a6d5a45f734acbfe1bf42ef209a92a5c217aeb383631bdb")
    version("2.13", sha256="bd90d6119bcc2898befd6e1bbb2cb1ed3bb1c2997d5eaa6fdbca4ee16191a906")
    version("2.12.2", sha256="6b7392a7b339a3f2db6e4bc8d5418cf29116d9e7e36b313e845cb65e449c5346")
    version("2.11.3", sha256="ddc3210f4029991f5142fda7f269f9bfb197917e5d9445ba2d90d31f74cc2765")
    version("2.10.1", sha256="cd9743db33389e7b4eb2942a4f365d12fc015f115113b230152280c43ccc7e3f")
    version("2.9", sha256="e0210dec2a4ca0a03d8ee26e2a4ebccc915d99f4cdb1489ff0f9f4ce7bda3e30")
    version("2.8", sha256="a5b91339355a7bbafc5f44b524556f7f25de83dd56f2c00ef9240dabd6865663")
    version("2.7", sha256="f5ef515cb70f8d4cfcee0b3aac05b73def60d897bdb7a71f4356782febfe415a")
    version("2.6.1", sha256="6be7639ccad715d25eef560ce9d1637ef206fb9a162714f6ab8167fc0d971cae")
    version("2.5", sha256="16d3ac4e86eed75d85d80f1f214a6bd58d27f13590966b5ad0cc181df85a3493")


    variant("stage2", default=False)
    provides("iconv", when="+stage2")

    # Fix for newer GCC, related to -fno-common
    patch("locs.patch", when="@2.23:2.25")
    patch("locs-2.22.patch", when="@:2.22")

    # _obstack_compat symbol is not initialized
    patch("39b1f61.patch", when="@:2.17")

    # docs: install fails with "unknown command hsep / vsep"
    patch("texi.patch", when="@2.16.0")

    # rpc/types.h include issue, should be from local version, not system.
    patch("fb21f89.patch", when="@:2.16")

    # Avoid linking libgcc_eh
    patch("95f5a9a-stub.patch", when="@:2.16")
    patch("95f5a9a-2.16.patch", when="@2.16")
    patch("95f5a9a-2.15.patch", when="@2.14:2.15")
    patch("95f5a9a-2.13.patch", when="@2.12:2.13")
    patch("95f5a9a-2.11.patch", when="@:2.11")

    # Use init_array (modified commit 4a531bb to unconditionally define
    # NO_CTORS_DTORS_SECTIONS)
    patch("4a531bb.patch", when="@:2.12")

    # make: mixed implicit and static pattern rules (trivial issue in docs)
    patch("32cf406.patch", when="@:2.10")

    # linker flag output regex
    patch("7c8a673.patch", when="@:2.9")

    # Use AT_RANDOM provided by the kernel instead of /dev/urandom;
    # recent gcc + binutils have issues with the inline assembly in
    # the fallback code, so better to use the kernel-provided value.
    patch("965cb60.patch", when="@2.8:2.9")
    patch("965cb60-2.7.patch", when="@2.7")
    patch("965cb60-2.6.patch", when="@2.6")
    patch("965cb60-2.5.patch", when="@2.5")

    # include_next <limits.h> not working
    patch("67fbfa5.patch", when="@:2.7")

    def setup_build_environment(self, env):
        if self.spec.satisfies("@:2.21"):
            env.append_flags("LDFLAGS", "-no-pie")
        if self.spec.satisfies("@:2.16"):
            # for some reason CPPFLAGS -U_FORTIFY_SOURCE is not enough, it has to be CFLAGS
            env.append_flags("CPPFLAGS", "-U_FORTIFY_SOURCE")
            env.append_flags("CFLAGS", "-O2 -g -fno-stack-protector -U_FORTIFY_SOURCE")
        if self.spec.satisfies("@:2.9"):
            # missing defines in elf.h after 965cb60.patch
            env.append_flags("CFLAGS", "-DAT_BASE_PLATFORM=24 -DAT_RANDOM=25")
        if self.spec.satisfies("@:2.6"):
            # change of defaults in gcc 10
            env.append_flags("CFLAGS", "-fcommon")
        if self.spec.satisfies("@2.5"):
            env.append_flags("CFLAGS", "-fgnu89-inline")

    def patch(self):
        # Support gmake >= 4
        filter_file(
            "    3.79* | 3.[89]*)",
            "    3.79* | 3.[89]* |  [4-9].* | [1-9][0-9]*)",
            "configure",
            string=True,
        )

        # Suport gcc >= 5
        filter_file(
            "3.4* | 4.[0-9]* )",
            "3.4* | 4.[0-9]* | [5-9].* | [1-9][0-9]*)",
            "configure",
            string=True,
        )

        # Support gcc >= 10
        filter_file(
            "4.[3-9].* | 4.[1-9][0-9].* | [5-9].* )",
            "4.[3-9].* | 4.[1-9][0-9].* | [5-9].* | [1-9][0-9]*)",
            "configure",
            string=True,
        )
        filter_file(
            "4.[4-9].* | 4.[1-9][0-9].* | [5-9].* )",
            "4.[4-9].* | 4.[1-9][0-9].* | [5-9].* | [1-9][0-9]*)",
            "configure",
            string=True,
        )

        # Support binutils
        filter_file(
            "2.1[3-9]*)",
            "2.1[3-9]*|2.1[0-9][0-9]*|2.[2-9][0-9]*|[3-9].*|[1-9][0-9]*)",
            "configure",
            string=True,
        )

    # This is an absolutely wretched hack to allow building a glibc that doesn't pollute
    # the new environment.  It should go away as soon as we have a way.
    with when("~stage2"):
        depends_on("bison", type="build")
        depends_on("texinfo", type="build")
        depends_on("gettext", type="build", when="~stage2")
        depends_on("perl", type="build")
        depends_on("gawk", type="build")
        depends_on("sed", type="build")
        depends_on("gmake", type="build")

        # See 2d7ed98add14f75041499ac189696c9bd3d757fe
        depends_on("gmake@:4.3", type="build", when="@:2.36")

        # From 2.29: generates locale/C-translit.h
        # before that it's a test dependency.
        depends_on("python@3.4:", type="build", when="@2.29:")

    # NOTE(trws): switched to build because glibc now copies the headers in. This is
    # mainly to avoid any issues with handling header directory ordering, with them in
    # separate roots it becomes very, very tricky.
    depends_on("linux-headers", type="build")

    with when("@master"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")

    def configure_args(self):
        return [
            "--enable-kernel=3.7.0",
            "--with-headers={}".format(self.spec["linux-headers"].prefix.include),
            "--without-selinux",
        ] + ([] if not self.spec.satisfies("os=spack") else [
                '--host='+self.spec.target_triple,
                '--build=' + self.spec.host_triple,
                # 'libc_cv_slibdir='+self.spec.prefix.lib,
                # 'rootsbindir='+self.spec.prefix.sbin,
                ])

    @property
    def ld_so(self):
        opts = glob.glob(f"{self.spec.prefix.lib.join('ld-linux')}*.so*")
        if opts:
            return opts[0]
        else:
            return None

    @property
    def dynamic_linker_flag(self):
        return f"-Wl,--dynamic-linker={self.ld_so}"

    def build(self, spec, prefix):
        # 1. build just ld.so
        # 2. drop the rpath from ld.so -- otherwise it cannot be executed
        # 3. do the rest of the build that may directly run ld.so
        with working_dir(self.build_directory):
            make("-C", "..", f"objdir={os.getcwd()}", "lib")
            delete_rpath(join_path("elf", "ld.so"))
            make()

    @run_after("install")
    def add_linux_headers(self):
        cp = which("cp")
        cp('-r', self.spec['linux-headers'].prefix.include, self.spec.prefix)
    @run_after("install")
    def install_locales(self):
        if self.spec.satisfies("os=spack"):
            ldef = Executable(self.prefix.bin.localedef, )
            mkdirp(self.spec.prefix.lib.locale)
            ldef("-i","POSIX","-f","UTF-8","C.UTF-8", fail_on_error=False)
            ldef("-i","cs_CZ","-f","UTF-8","cs_CZ.UTF-8")
            ldef("-i","de_DE","-f","ISO-8859-1","de_DE")
            ldef("-i","de_DE@euro","-f","ISO-8859-15","de_DE@euro")
            ldef("-i","de_DE","-f","UTF-8","de_DE.UTF-8")
            ldef("-i","el_GR","-f","ISO-8859-7","el_GR")
            ldef("-i","en_GB","-f","ISO-8859-1","en_GB")
            ldef("-i","en_GB","-f","UTF-8","en_GB.UTF-8")
            ldef("-i","en_HK","-f","ISO-8859-1","en_HK")
            ldef("-i","en_PH","-f","ISO-8859-1","en_PH")
            ldef("-i","en_US","-f","ISO-8859-1","en_US")
            ldef("-i","en_US","-f","UTF-8","en_US.UTF-8")
            ldef("-i","es_ES","-f","ISO-8859-15","es_ES@euro")
            ldef("-i","es_MX","-f","ISO-8859-1","es_MX")
            ldef("-i","fa_IR","-f","UTF-8","fa_IR")
            ldef("-i","fr_FR","-f","ISO-8859-1","fr_FR")
            ldef("-i","fr_FR@euro","-f","ISO-8859-15","fr_FR@euro")
            ldef("-i","fr_FR","-f","UTF-8","fr_FR.UTF-8")
            ldef("-i","is_IS","-f","ISO-8859-1","is_IS")
            ldef("-i","is_IS","-f","UTF-8","is_IS.UTF-8")
            ldef("-i","it_IT","-f","ISO-8859-1","it_IT")
            ldef("-i","it_IT","-f","ISO-8859-15","it_IT@euro")
            ldef("-i","it_IT","-f","UTF-8","it_IT.UTF-8")
            ldef("-i","ja_JP","-f","EUC-JP","ja_JP")
            ldef("-i","ja_JP","-f","SHIFT_JIS","ja_JP.SJIS", fail_on_error=False)
            ldef("-i","ja_JP","-f","UTF-8","ja_JP.UTF-8")
            ldef("-i","nl_NL@euro","-f","ISO-8859-15","nl_NL@euro")
            ldef("-i","ru_RU","-f","KOI8-R","ru_RU.KOI8-R")
            ldef("-i","ru_RU","-f","UTF-8","ru_RU.UTF-8")
            ldef("-i","se_NO","-f","UTF-8","se_NO.UTF-8")
            ldef("-i","ta_IN","-f","UTF-8","ta_IN.UTF-8")
            ldef("-i","tr_TR","-f","UTF-8","tr_TR.UTF-8")
            ldef("-i","zh_CN","-f","GB18030","zh_CN.GB18030")
            ldef("-i","zh_HK","-f","BIG5-HKSCS","zh_HK.BIG5-HKSCS")
            ldef("-i","zh_TW","-f","UTF-8","zh_TW.UTF-8")
