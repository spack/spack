# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dfelibs(CMakePackage):
    """Dr. Fred Edison's incredible useful C++14 libraries."""

    homepage = "https://github.com/acts-project/dfelibs"
    url = "https://github.com/acts-project/dfelibs/archive/refs/tags/v20200330.tar.gz"

    maintainers("HadrienG2", "stephenswat", "wdconinc")

    version("20231012", sha256="7127069858c2e3ce663e66f45e3f7e02ede8bbca23d90f6c89f43f5b05c44dcb")
    version("20211029", sha256="65b8d536b06b550e38822905dea06d193beb703fe0e4442791f43dc087c5cbfb")
    version("20200416", sha256="19fdd75eee88d3fa19feaa27b9a8f9aebf9c58e8cd266d136e13e857ac984e82")
    version("20200330", sha256="856e01cf5a42e36798c1d24b4d035ac77ecd9015bc9024c6f554a11302841440")