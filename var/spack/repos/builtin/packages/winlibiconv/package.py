# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.build_systems.generic import GenericBuilder
from spack.package import *


class Winlibiconv(Package, SourceforgePackage):
    """Windows GNUWIN32 project port of GNU libiconv provides an
    implementation of the iconv() function
    and the iconv program for character set conversion."""

    homepage = "https://gnuwin32.sourceforge.net/packages/libiconv.htm"
    sourceforge_mirror_path = "gnuwin32/files/libiconv-1.8-src.zip"

    version("1.8", sha256="1da58752373f8234744f246e38d8fdc1ad70c7593da5a229305fbae63b36f334")
    version("1.7", sha256="cb548cba97e2d1f667d2ccd7b9929094d5b50aba26864b970551552afbf5743d")
    version("1.6.1", sha256="69c63e2208af97c8795d3ffe81a384712f1d5fe6f2d33e59d9bbb291c8902752")
    version("1.6", sha256="c2023bdd9225f9b794085645de0f717634ed411962981e87c83444cb2491af2c")

    provides("iconv")

    for plat in ["linux", "darwin", "cray"]:
        conflicts(plat)


class NMakeBuilder(GenericBuilder):
    def build(self, pkg, spec, prefix):
        file_root = glob.glob(os.path.join(self.stage.source_path, "src", "libiconv-*"))[0]
        with working_dir(file_root):
            nmake("-f", "%s\\Makefile.msvc" % file_root)

    def install(self, pkg, spec, prefix):
        file_root = glob.glob(os.path.join(self.stage.source_path, "src", "libiconv-*"))[0]
        with working_dir(file_root):
            file_root = glob.glob(os.path.join("src", "libiconv-*"))[0]
            nmake(
                "-f",
                "%s\\Makefile.msvc" % file_root,
                "install",
                "PREFIX=%s" % prefix,
            )
