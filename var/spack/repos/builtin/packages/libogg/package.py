# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libogg(AutotoolsPackage):
    """Ogg is a multimedia container format, and the native file and stream
    format for the Xiph.org multimedia codecs."""

    homepage = "https://www.xiph.org/ogg/"
    url = "http://downloads.xiph.org/releases/ogg/libogg-1.3.2.tar.gz"

    version("1.3.5", sha256="0eb4b4b9420a0f51db142ba3f9c64b333f826532dc0f48c6410ae51f4799b664")
    version("1.3.4", sha256="fe5670640bd49e828d64d2879c31cb4dde9758681bb664f9bdbf159a01b0c76e")
    version("1.3.2", sha256="e19ee34711d7af328cb26287f4137e70630e7261b17cbe3cd41011d73a654692")

    # Backport a patch that fixes an unsigned typedef problem on macOS:
    # https://github.com/xiph/ogg/pull/64
    patch(
        "https://github.com/xiph/ogg/commit/c8fca6b4a02d695b1ceea39b330d4406001c03ed.patch?full_index=1",
        sha256="0f4d289aecb3d5f7329d51f1a72ab10c04c336b25481a40d6d841120721be485",
        when="@1.3.4 platform=darwin",
    )
