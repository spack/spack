# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Rhash(MakefilePackage, AutotoolsPackage):
    """RHash is a console utility for computing and verifying hash sums of
    files. It supports CRC32, MD4, MD5, SHA1, SHA256, SHA512, SHA3, Tiger,
    TTH, Torrent BTIH, AICH, ED2K, GOST R 34.11-94, RIPEMD-160, HAS-160,
    EDON-R 256/512, WHIRLPOOL and SNEFRU hash sums."""

    homepage = "https://sourceforge.net/projects/rhash/"
    url = "https://github.com/rhash/RHash/archive/v1.3.5.tar.gz"

    version("1.4.4", sha256="8e7d1a8ccac0143c8fe9b68ebac67d485df119ea17a613f4038cda52f84ef52a")
    version("1.4.3", sha256="1e40fa66966306920f043866cbe8612f4b939b033ba5e2708c3f41be257c8a3e")
    version("1.4.2", sha256="600d00f5f91ef04194d50903d3c79412099328c42f28ff43a0bdb777b00bec62")
    version("1.3.5", sha256="98e0688acae29e68c298ffbcdbb0f838864105f9b2bd8857980664435b1f1f2e")

    build_system(
        conditional("autotools", when="@1.4:"),
        conditional("makefile", when="@:1.3"),
        default="autotools",
    )

    # Intel 20xx.yy.z works just fine.  Un-block it from the configure script
    # https://github.com/rhash/RHash/pull/197
    patch("rhash-intel20.patch", when="@1.3.6:1.4.2")


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder):
    def build(self, pkg, spec, prefix):
        # Doesn't build shared libraries by default
        make("PREFIX={0}".format(prefix))

        if spec.satisfies("platform=darwin"):
            make("PREFIX={0}".format(prefix), "-C", "librhash", "dylib")
        else:
            make("PREFIX={0}".format(prefix), "lib-shared")

    def install(self, pkg, spec, prefix):
        # Some things are installed to $(DESTDIR)$(PREFIX) while other things
        # are installed to $DESTDIR/etc.
        make("install", "DESTDIR={0}".format(prefix), "PREFIX=")
        make("install-lib-static", "DESTDIR={0}".format(prefix), "PREFIX=")

        if spec.satisfies("platform=darwin"):
            install("librhash/*.dylib", prefix.lib)
        else:
            make("install-lib-shared", "DESTDIR={0}".format(prefix), "PREFIX=")
            os.symlink(
                join_path(prefix.lib, "librhash.so.0"), join_path(prefix.lib, "librhash.so")
            )


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):
    pass
