# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TlExpected(CMakePackage):
    """C++11/14/17 std::expected with functional-style extensions."""

    homepage = "https://tl.tartanllama.xyz/en/latest/"
    git = "https://github.com/TartanLlama/expected.git"

    maintainers = ["charmoniumQ"]

    version("master", branch="master")
    version("1.0.0", sha256="8f5124085a124113e75e3890b4e923e3a4de5b26a973b891b3deb40e19c03cee")
