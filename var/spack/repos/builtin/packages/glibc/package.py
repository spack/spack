# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.util.elf import delete_rpath


class Glibc(AutotoolsPackage, GNUMirrorPackage):
    """The GNU C Library provides many of the low-level components used
    directly by programs written in the C or C++ languages."""

    homepage = "https://www.gnu.org/software/libc/"
    gnu_mirror_path = "libc/glibc-2.33.tar.gz"
    git = "https://sourceware.org/git/glibc.git"

    maintainers("haampie")

    build_directory = "build"

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
    version("2.14", sha256="4812ddcedb5270869ef97c165980af5b459f3986dd5d420a5eb749171c8facec")
    version("2.13", sha256="bd90d6119bcc2898befd6e1bbb2cb1ed3bb1c2997d5eaa6fdbca4ee16191a906")
    version("2.12.2", sha256="6b7392a7b339a3f2db6e4bc8d5418cf29116d9e7e36b313e845cb65e449c5346")
    version("2.12.1", sha256="5ae2edf67169aac932a281cbe636f8be42a854cc3d8b7f325c53b949eab72d48")

    # Fix for newer GCC, related to -fno-common
    patch("locs.patch", when="@2.23:2.25")
    patch("locs-2.22.patch", when="@:2.22")

    # _obstack_compat symbol is not initialized
    patch("39b1f61.patch", when="@:2.17")

    # Install fails with "unknown command hsep / vsep"
    patch("texi.patch", when="@2.16.0")

    # rpc/types.h include issue
    patch("fb21f89.patch", when="@:2.16")

    def patch(self):
        # Deal with Make version detection not taking into account >= 4.x
        filter_file(
            "    3.79* | 3.[89]*)",
            "    3.79* | 3.[89]* |  [4-9].* | [1-9][0-9]*)",
            "configure",
            string=True,
        )

        # Similarly: gcc >= 5 was not anticipated.
        filter_file(
            "3.4* | 4.[0-9]* )",
            "3.4* | 4.[0-9]* | [5-9].* | [1-9][0-9]*)",
            "configure",
            string=True,
        )

    depends_on("bison", type="build")
    depends_on("texinfo", type="build")
    depends_on("gettext", type="build")

    # The GCC 10 issue here is not necessarily a build issue, but a broken configure
    # script that cannot deal with multi-digit major versions.
    conflicts("%gcc@10:", when="@:2.20")

    with when("@master"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")

    def build(self, spec, prefix):
        # First build just the dynamic linker, and strip its rpath that Spack likes to
        # add -- it will cause the dynamic linker to error when being executed.
        with working_dir(self.build_directory):
            make("-C", "..", f"objdir={os.getcwd()}", "lib")
            delete_rpath("elf/ld.so")
            make()
